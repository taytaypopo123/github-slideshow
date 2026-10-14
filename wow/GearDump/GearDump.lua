-- GearDump: snapshots equipped gear, equippable bag items and key stats into
-- GearDumpDB. WoW only writes SavedVariables to disk on /reload or logout.

local SLOTS = {
  "HeadSlot", "NeckSlot", "ShoulderSlot", "BackSlot", "ChestSlot", "ShirtSlot",
  "TabardSlot", "WristSlot", "HandsSlot", "WaistSlot", "LegsSlot", "FeetSlot",
  "Finger0Slot", "Finger1Slot", "Trinket0Slot", "Trinket1Slot",
  "MainHandSlot", "SecondaryHandSlot", "RangedSlot", "AmmoSlot",
}

local function itemInfo(link)
  if not link then return nil end
  return {
    id = tonumber(link:match("item:(%d+)")),
    name = link:match("%[(.-)%]"),
    link = link,
  }
end

-- Container API moved to C_Container in newer clients; support both.
local NumSlots = (C_Container and C_Container.GetContainerNumSlots) or GetContainerNumSlots
local ItemLink = (C_Container and C_Container.GetContainerItemLink) or GetContainerItemLink
local IsEquippable = (C_Item and C_Item.IsEquippableItem) or IsEquippableItem

local function safe(fn, ...)
  if not fn then return nil end
  local ok, a, b = pcall(fn, ...)
  if ok then return a, b end
end

local function snapshot()
  local name, realm = UnitName("player"), GetRealmName()
  local snap = {
    name = name,
    realm = realm,
    level = UnitLevel("player"),
    class = select(2, UnitClass("player")),
    race = select(2, UnitRace("player")),
    saved = date("%Y-%m-%d %H:%M:%S"),
    equipped = {},
    bags = {},
    stats = {},
  }

  for _, slot in ipairs(SLOTS) do
    local slotId = GetInventorySlotInfo(slot)
    if slotId then
      snap.equipped[slot] = itemInfo(GetInventoryItemLink("player", slotId))
    end
  end

  if NumSlots and ItemLink then
    for bag = 0, 4 do
      for i = 1, (NumSlots(bag) or 0) do
        local link = ItemLink(bag, i)
        if link and IsEquippable and IsEquippable(link) then
          table.insert(snap.bags, itemInfo(link))
        end
      end
    end
  end

  local s = snap.stats
  s.health = UnitHealthMax("player")
  s.mana = UnitPowerMax("player", 0)
  s.strength = select(2, UnitStat("player", 1))
  s.agility = select(2, UnitStat("player", 2))
  s.stamina = select(2, UnitStat("player", 3))
  s.intellect = select(2, UnitStat("player", 4))
  s.spirit = select(2, UnitStat("player", 5))
  s.armor = select(2, UnitArmor("player"))
  local rapBase, rapPos, rapNeg = safe(UnitRangedAttackPower, "player")
  if rapBase then s.rangedAP = rapBase + (rapPos or 0) + (rapNeg or 0) end
  s.rangedCrit = safe(GetRangedCritChance)
  s.meleeCrit = safe(GetCritChance)

  GearDumpDB = GearDumpDB or {}
  GearDumpDB[name .. "-" .. realm] = snap
  return snap
end

local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_LOGIN")
f:RegisterEvent("PLAYER_EQUIPMENT_CHANGED")
f:RegisterEvent("PLAYER_LOGOUT")
f:SetScript("OnEvent", function() snapshot() end)

SLASH_GEARDUMP1 = "/geardump"
SlashCmdList.GEARDUMP = function()
  local snap = snapshot()
  local n = 0
  for _ in pairs(snap.equipped) do n = n + 1 end
  print(("|cff8a5712GearDump|r: captured %d equipped items and %d bag items. Type /reload to save to disk."):format(n, #snap.bags))
end

-- /qscan <from> <to> [batch] [delay]: asks the server for quest data across
-- a range of quest IDs and saves every title it gets to GearDumpQuests. The
-- server drops requests that come too fast, so this sends small batches with a
-- long wait, records titles as QUEST_DATA_LOAD_RESULT replies arrive, then runs
-- a slower second pass over only the IDs that came back empty.
local QuestTitle = C_QuestLog and (C_QuestLog.GetTitleForQuestID or C_QuestLog.GetQuestInfo)
local RequestQuest = C_QuestLog and C_QuestLog.RequestLoadQuestByID
local DEFAULT_BATCH, DEFAULT_DELAY = 10, 3
local RETRY_BATCH, RETRY_DELAY = 5, 4

local function saveTitle(id)
  local ok, title = pcall(QuestTitle, id)
  if ok and title and title ~= "" then
    GearDumpQuests[id] = title
    return true
  end
end

local qf = CreateFrame("Frame")
qf:RegisterEvent("QUEST_DATA_LOAD_RESULT")
qf:SetScript("OnEvent", function(_, _, id, success)
  if success and GearDumpQuests and QuestTitle then saveTitle(id) end
end)

local function countTitles()
  local n = 0
  for _ in pairs(GearDumpQuests) do n = n + 1 end
  return n
end

local scanning = false

SLASH_GEARDUMPQSCAN1 = "/qscan"
SlashCmdList.GEARDUMPQSCAN = function(msg)
  if not QuestTitle then
    print("|cff8a5712GearDump|r: this client has no quest title lookup.")
    return
  end
  if scanning then
    print("|cff8a5712GearDump|r: a scan is already running.")
    return
  end
  local from, to, batch, delay = msg:match("(%d+)%s+(%d+)%s*(%d*)%s*([%d%.]*)")
  from, to = tonumber(from) or 90000, tonumber(to) or 98000
  batch, delay = tonumber(batch) or DEFAULT_BATCH, tonumber(delay) or DEFAULT_DELAY
  GearDumpQuests = GearDumpQuests or {}
  local ids = {}
  for id = from, to do ids[#ids + 1] = id end
  scanning = true
  print(("|cff8a5712GearDump|r: scanning quests %d-%d, %d every %ss (first pass about %d min)..."):format(
    from, to, batch, delay, math.ceil(#ids / batch * delay / 60)))

  local function pass(list, size, wait, label, onDone)
    local misses, pos, nextReport = {}, 1, 0.25
    local function step()
      local last = math.min(pos + size - 1, #list)
      if RequestQuest then
        for k = pos, last do pcall(RequestQuest, list[k]) end
      end
      C_Timer.After(wait, function()
        for k = pos, last do
          if not saveTitle(list[k]) then misses[#misses + 1] = list[k] end
        end
        pos = last + 1
        if pos / #list >= nextReport and pos <= #list then
          print(("|cff8a5712GearDump|r: %s %d%%, %d titles so far."):format(label, math.floor(nextReport * 100), countTitles()))
          nextReport = nextReport + 0.25
        end
        if pos <= #list then step() else onDone(misses) end
      end)
    end
    step()
  end

  local function finish()
    scanning = false
    print(("|cff8a5712GearDump|r: done. %d quest titles saved. Type /reload to write them to disk."):format(countTitles()))
  end

  pass(ids, batch, delay, "first pass", function(misses)
    if #misses == 0 then return finish() end
    print(("|cff8a5712GearDump|r: retrying %d empty IDs, %d every %ss (about %d min)..."):format(
      #misses, RETRY_BATCH, RETRY_DELAY, math.ceil(#misses / RETRY_BATCH * RETRY_DELAY / 60)))
    pass(misses, RETRY_BATCH, RETRY_DELAY, "retry pass", finish)
  end)
end

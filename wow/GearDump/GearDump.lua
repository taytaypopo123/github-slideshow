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
        if link and IsEquippableItem(link) then
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

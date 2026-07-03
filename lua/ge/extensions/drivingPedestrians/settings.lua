local M = {}

M.autoEnableDrivers = true
M.autoEnablePassengers = false
M.applyToTraffic = true
M.applyToAI = true
M.driverSkin = "dped_skin_casual_m"
M.passengerPart = "dped_passenger_empty"
M.showStartupMessage = true

local SETTINGS_FILE = "settings/drivingPedestrians.json"

local function loadFromDisk()
  local data = jsonReadFile(SETTINGS_FILE)
  if type(data) ~= "table" then
    return
  end
  for key, value in pairs(data) do
    if M[key] ~= nil then
      M[key] = value
    end
  end
end

local function saveToDisk()
  local data = {
    autoEnableDrivers = M.autoEnableDrivers,
    autoEnablePassengers = M.autoEnablePassengers,
    applyToTraffic = M.applyToTraffic,
    applyToAI = M.applyToAI,
    driverSkin = M.driverSkin,
    passengerPart = M.passengerPart,
    showStartupMessage = M.showStartupMessage
  }
  jsonWriteFile(SETTINGS_FILE, data, true)
end

function M.load()
  loadFromDisk()
end

function M.save()
  saveToDisk()
end

function M.toggleAutoDrivers()
  M.autoEnableDrivers = not M.autoEnableDrivers
  saveToDisk()
  return M.autoEnableDrivers
end

function M.toggleTraffic()
  M.applyToTraffic = not M.applyToTraffic
  saveToDisk()
  return M.applyToTraffic
end

return M

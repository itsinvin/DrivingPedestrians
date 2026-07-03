local M = {}

M.dependencies = {"drivingPedestrians_settings", "drivingPedestrians_vehicleOffsets"}

local settings = drivingPedestrians_settings
local offsets = drivingPedestrians_vehicleOffsets

local pendingVehicles = {}
local initialized = false

local function logInfo(msg)
  log("I", "drivingPedestrians", msg)
end

local function shouldProcessVehicle(veh)
  if not veh then
    return false
  end

  local model = veh:getJBeamFilename()
  if not model or model == "" then
    return false
  end

  if model == "agenty_dummy" or model == "simple_traffic" then
    return false
  end

  if veh:isPlayerControlled() then
    return settings.autoEnableDrivers
  end

  if settings.applyToTraffic or settings.applyToAI then
    return true
  end

  return false
end

local function readVehicleConfig(veh)
  local partConfigField = veh.partConfig or veh:getField("partConfig", 0) or ""
  if partConfigField == "" then
    return {parts = {}, vars = {}}
  end

  local ok, decoded = pcall(jsonDecode, partConfigField)
  if not ok or type(decoded) ~= "table" then
    return {parts = {}, vars = {}}
  end

  decoded.parts = decoded.parts or {}
  decoded.vars = decoded.vars or {}
  return decoded
end

local function buildDriverConfig(veh)
  local model = veh:getJBeamFilename()
  local driverInfo = offsets.getDriverInfo(model)
  if not driverInfo then
    return nil
  end

  local config = readVehicleConfig(veh)
  if offsets.hasDriverInstalled(config.parts, driverInfo.slot) then
    return nil
  end

  config.parts[driverInfo.slot] = driverInfo.part
  if settings.driverSkin and settings.driverSkin ~= "" then
    config.parts.dped_driver_skin = settings.driverSkin
  end
  if settings.autoEnablePassengers and settings.passengerPart and settings.passengerPart ~= "" then
    config.parts.dped_passenger_slot = settings.passengerPart
  end
  return config
end

local function applyDriverToVehicle(vehId)
  local veh = be:getObjectByID(vehId)
  if not veh or not shouldProcessVehicle(veh) then
    return
  end

  local config = buildDriverConfig(veh)
  if not config then
    return
  end

  if veh:isPlayerControlled() and extensions.core_vehicle_partmgmt then
    local current = extensions.core_vehicle_partmgmt.getConfig()
    if not current or not current.parts then
      return
    end

    local driverInfo = offsets.getDriverInfo(veh:getJBeamFilename())
    if offsets.hasDriverInstalled(current.parts, driverInfo.slot) then
      return
    end

    current.parts[driverInfo.slot] = driverInfo.part
    if settings.driverSkin and settings.driverSkin ~= "" then
      current.parts.dped_driver_skin = settings.driverSkin
    end
    if settings.autoEnablePassengers and settings.passengerPart and settings.passengerPart ~= "" then
      current.parts.dped_passenger_slot = settings.passengerPart
    end

    extensions.core_vehicle_partmgmt.setPartsConfig(current.parts, true)
    logInfo("Added pedestrian driver to player vehicle: " .. tostring(veh:getJBeamFilename()))
    return
  end

  local encoded = jsonEncode(config)
  if not encoded then
    return
  end

  veh:setField("partConfig", 0, encoded)
  veh:requestReset(RESET_PHYSICS)
  logInfo("Added pedestrian driver to vehicle: " .. tostring(veh:getJBeamFilename()))
end

local function processPending()
  if not next(pendingVehicles) then
    return
  end

  for vehId, _ in pairs(pendingVehicles) do
    pendingVehicles[vehId] = nil
    applyDriverToVehicle(vehId)
  end
end

local function queueVehicle(vehId)
  if not vehId or vehId <= 0 then
    return
  end
  pendingVehicles[vehId] = true
end

local function onVehicleSpawned(vehId)
  if not settings.autoEnableDrivers and not settings.applyToTraffic then
    return
  end
  queueVehicle(vehId)
end

local function onVehicleResetted(vehId)
  if not settings.autoEnableDrivers and not settings.applyToTraffic then
    return
  end
  queueVehicle(vehId)
end

local function onExtensionLoaded()
  settings.load()
  initialized = true
  if settings.showStartupMessage then
    logInfo("Driving Pedestrians loaded. Drivers auto-enable: " .. tostring(settings.autoEnableDrivers))
    logInfo("Use Parts > Additional Modification > Pedestrian Driver for manual placement.")
    logInfo("Press Ctrl+D to toggle auto-drivers.")
  end
end

local function onUpdate()
  if not initialized then
    return
  end
  processPending()
end

local function onSerialize()
  return {autoEnableDrivers = settings.autoEnableDrivers}
end

local function onDeserialize(data)
  if type(data) == "table" and data.autoEnableDrivers ~= nil then
    settings.autoEnableDrivers = data.autoEnableDrivers
    settings.save()
  end
end

local function toggleAutoDrivers()
  local enabled = settings.toggleAutoDrivers()
  guihooks.trigger("drivingPedestriansAutoDriversChanged", enabled)
  if enabled then
    for i = 0, be:getObjectCount() - 1 do
      local veh = be:getObject(i)
      if veh and veh:getClassName() == "BeamNGVehicle" then
        queueVehicle(veh:getID())
      end
    end
  end
  return enabled
end

M.onExtensionLoaded = onExtensionLoaded
M.onUpdate = onUpdate
M.onVehicleSpawned = onVehicleSpawned
M.onVehicleResetted = onVehicleResetted
M.onSerialize = onSerialize
M.onDeserialize = onDeserialize
M.toggleAutoDrivers = toggleAutoDrivers
M.applyDriverToFocusedVehicle = function()
  local veh = be:getPlayerVehicle(0)
  if veh then
    applyDriverToVehicle(veh:getID())
  end
end

return M

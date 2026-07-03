local M = {}

-- Maps BeamNG vehicle model names to driver part names and mod slot keys.
M.vehicleDriverParts = {
  pickup = {slot = "pickup_mod", part = "dped_pickup_driver"},
  hseries = {slot = "hseries_mod", part = "dped_hseries_driver"},
  roamer = {slot = "roamer_mod", part = "dped_roamer_driver"},
  etk800 = {slot = "etk800_mod", part = "dped_etk800_driver"},
  etkc = {slot = "etkc_mod", part = "dped_etkc_driver"},
  etki = {slot = "etki_mod", part = "dped_etki_driver"},
  coupe = {slot = "coupe_mod", part = "dped_coupe_driver"},
  fullsize = {slot = "fullsize_mod", part = "dped_fullsize_driver"},
  barstow = {slot = "barstow_mod", part = "dped_barstow_driver"},
  bluebuck = {slot = "bluebuck_mod", part = "dped_bluebuck_driver"},
  burnside = {slot = "burnside_mod", part = "dped_burnside_driver"},
  moonhawk = {slot = "moonhawk_mod", part = "dped_moonhawk_driver"},
  pessima = {slot = "pessima_mod", part = "dped_pessima_driver"},
  pessima2 = {slot = "pessima2_mod", part = "dped_pessima2_driver"},
  legran = {slot = "legran_mod", part = "dped_legran_driver"},
  vivace = {slot = "vivace_mod", part = "dped_vivace_driver"},
  wendover = {slot = "wendover_mod", part = "dped_wendover_driver"},
  scintilla = {slot = "scintilla_mod", part = "dped_scintilla_driver"},
  sunburst = {slot = "sunburst_mod", part = "dped_sunburst_driver"},
  sunburst2 = {slot = "sunburst2_mod", part = "dped_sunburst2_driver"},
  covet = {slot = "covet_mod", part = "dped_covet_driver"},
  miramar = {slot = "miramar_mod", part = "dped_miramar_driver"},
  hopper = {slot = "hopper_mod", part = "dped_hopper_driver"},
  midsize = {slot = "midsize_mod", part = "dped_midsize_driver"},
  bastion = {slot = "bastion_mod", part = "dped_bastion_driver"},
  autobello = {slot = "autobello_mod", part = "dped_autobello_driver"},
  lansdale = {slot = "lansdale_mod", part = "dped_lansdale_driver"},
  us_semi = {slot = "us_semi_mod", part = "dped_us_semi_driver"},
  citybus = {slot = "citybus_mod", part = "dped_citybus_driver"}
}

M.genericDriverPart = "dped_generic_driver"

function M.getDriverInfo(model)
  if not model then
    return nil
  end
  local info = M.vehicleDriverParts[model]
  if info then
    return info
  end
  return {slot = model .. "_mod", part = M.genericDriverPart}
end

function M.hasDriverInstalled(parts, slotName)
  if type(parts) ~= "table" or not slotName then
    return false
  end
  local installed = parts[slotName]
  if not installed or installed == "" then
    return false
  end
  return string.find(installed, "dped_") ~= nil
end

return M

local M = {}

-- Subtle driver head movement while the vehicle is moving.
local lastSpeed = 0
local lookTimer = 0

local function getSpeedKmh()
  local velocity = obj:getVelocity()
  if not velocity then
    return 0
  end
  return velocity:length() * 3.6
end

function M.updateGFX(dt)
  if not electrics or not electrics.values then
    return
  end

  local speed = getSpeedKmh()
  lookTimer = lookTimer + dt

  if speed > 2 then
    local sway = math.sin(lookTimer * 1.7) * math.min(speed / 80, 1) * 2.5
    electrics.values.dpedHeadSway = sway
  else
    electrics.values.dpedHeadSway = 0
  end

  lastSpeed = speed
end

return M

# Van Status Guidelines

## Status Values
Vans can only have two status values:
- `available`: The van is available for use
- `not available`: The van is not available for use

## Status Determination Rules

### Available Status
A van should be marked as `available` when:

- It is explicitly marked as "en rotación" (in rotation)
- It has minor issues that don't affect operation (e.g., cosmetic damage)
- It has door issues but is still operational (especially van-7)
- Repairs have been completed (e.g., "tiene goma nueva" = "has new tire")
- Thread replies indicate an issue has been fixed
- A checkmark emoji (✅) has been added to a message about an issue, indicating it's resolved

### Not Available Status
A van should be marked as `not available` when:

- It is explicitly marked as "fuera de rotación" (out of rotation)
- It has a flat tire or tire issue with no confirmation of fix (e.g., "Se esta vaciando la goma")
- It has a major mechanical issue that prevents operation
- It is undergoing maintenance with no confirmation of completion

### Special Cases
- **Van-7**: Always mark as `available` even when it has door issues, as it's still operational

## Status Update Procedure
1. Check the most recent messages in the van's Slack channel
2. If a message mentions an issue, check for thread replies that might indicate the issue is resolved
3. If unclear, check for emoji reactions that might indicate status
4. Default to the previous known status if the current status cannot be determined

## Examples

| Message | Thread Replies | Status |
|---------|---------------|--------|
| "en rotación" | (none) | available |
| "fuera de rotación" | (none) | not available |
| "Se esta vaciando la goma" | "Ya tiene goma nueva" | available |
| "Problema con la puerta" for van-7 | (any/none) | available |
| "Problema con el motor" | (none) | not available |
| "Problema con el motor" | "Ya está arreglado" | available | 
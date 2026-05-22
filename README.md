# alfred-timeleft

Alfred workflow that shows how much of the current week, month, quarter, and year has elapsed and how much remains. Useful as a barometer for revenue/selling days when matched against graphs.

## Install

Download `timeleft.alfredworkflow` from the [latest release](https://github.com/jaacob/alfred-timeleft/releases) and double-click to install.

## Usage

Type `timeleft` in Alfred. Press Enter on any row to copy it, or pick "Copy all" to copy every visible line.

## Configuration

Open the workflow in Alfred Preferences and click the [x] (Configure Workflow) icon. Each period can be toggled on/off and independently set to count business days only (Mon-Fri) or all calendar days. Defaults: every period on, business days on.

The "Year-end date" field is optional and useful if your year effectively ends before December 31 (e.g. an annual shutdown). Enter a date as `YYYY-MM-DD` or leave it blank for Dec 31. Each January, the saved date auto-resets — until you enter a new date in the current year (or clear the field), a reminder row appears in the results.

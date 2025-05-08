// This was a quick script I put together to get Oasys T-HIS to read in multiple Interior Head Impact (IHI) head acceleration curves
//   The user would open T-HIS manually and then run this script from T-HIS
//   - The script would read in all the listed .cur (curve) files
//   - Then it will set the graph properties
//   - Then for each curve it will calculate the 3ms clip value and set a unique colour (cycling back to the 1st colour when all 30 colours have been used)
//
// The end result is a graph with all uniquely coloured curves overlaid, and 3ms clip values displayed
//
// List of .cur files
// Backslashes must either be doubled ( \\ = \ ) or replaced with forward slashes
const cur_list=[
"P:/Project/Head_Impact/IHI/Phase/Iteration000/Project_Phase_Iteration_Pos01/Project_Phase_Iteration000_Pos01_19071/_Reporter_Output/Project_Phase_Iteration000_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project/Head_Impact/IHI/Phase/Iteration010/Project_Phase_Iteration010_Pos01/Project_Phase_Iteration010_Pos01_21206/_Reporter_Output/Project_Phase_Iteration010_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project/Head_Impact/IHI/Phase/Iteration011/Project_Phase_Iteration011_Pos01/Project_Phase_Iteration011_Pos01_19313/_Reporter_Output/Project_Phase_Iteration011_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project/Head_Impact/IHI/Phase/Iteration012/Project_Phase_Iteration012_Pos01/Project_Phase_Iteration012_Pos01_19386/_Reporter_Output/Project_Phase_Iteration012_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project/Head_Impact/IHI/Phase/Iteration012a/Project_Phase_Iteration012a_Pos01/Project_Phase_Iteration012a_Pos01_21243/_Reporter_Output/Project_Phase_Iteration012a_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project/Head_Impact/IHI/Phase/Iteration012b/Project_Phase_Iteration012b_Pos01/Project_Phase_Iteration012b_Pos01_20964/_Reporter_Output/Project_Phase_Iteration012b_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project/Head_Impact/IHI/Phase/Iteration012c/Project_Phase_Iteration012c_Pos01/Project_Phase_Iteration012c_Pos01_20934/_Reporter_Output/Project_Phase_Iteration012c_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project/Head_Impact/IHI/Phase/Iteration013/Project_Phase_Iteration013_Pos01/Project_Phase_Iteration013_Pos01_19510/_Reporter_Output/Project_Phase_Iteration013_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project/Head_Impact/IHI/Phase/Iteration014/Project_Phase_Iteration014_Pos01/Project_Phase_Iteration014_Pos01_19930/_Reporter_Output/Project_Phase_Iteration014_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project/Head_Impact/IHI/Phase/Iteration030/Project_Phase_Iteration030_Pos01/Project_Phase_Iteration030_Pos01_21278/_Reporter_Output/Project_Phase_Iteration030_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project/Head_Impact/IHI/Phase/Iteration030a/Project_Phase_Iteration030a_Pos01/Project_Phase_Iteration030a_Pos01_21957/_Reporter_Output/Project_Phase_Iteration030a_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project/Head_Impact/IHI/Phase/Iteration031/Project_Phase_Iteration031_Pos01/Project_Phase_Iteration031_Pos01_21341/_Reporter_Output/Project_Phase_Iteration031_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project/Head_Impact/IHI/Phase/Iteration032/Project_Phase_Iteration032_Pos01/Project_Phase_Iteration032_Pos01_21927/_Reporter_Output/Project_Phase_Iteration032_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
]

// Read curves
// Set variables to .cur files. All backslashes must be doubled
for (let i = 0; i < cur_list.length; i++) {
  Read.Cur(cur_list[i]);
}

// Graph properties: legend auto layout, 1 column, x-axis general number format with 3 decimal places, y-axis general number format with 0 decimal places
var num = Graph.Total();
var graph = Graph.GetFromID(num);
graph.x_unit_decimals = 3;                             // 3 decimal places on x-axis
graph.y_unit_decimals = 0;                             // 0 decimal places on y-axis
graph.legend_layout = Graph.LEGEND_AUTO;               // Legend auto layout
//graph.num_legend_columns = Graph.LEGEND_1_COLUMN;
graph.background_colour = 1;                           // Set background colour
graph.foreground_colour = 14;                          // Set foreground colour
graph.x_unit_format = Graph.AXIS_UNITS_GENERAL;        // Set x axis units to general (i.e. not scientific)
graph.y_unit_format = Graph.AXIS_UNITS_GENERAL;        // Set y axis units to general (i.e. not scientific)
// Auto-confirm on
Options.auto_confirm = true;
// Calculate 3ms clip for all curves
// Also set the colour for each curve
var curve = Curve.First();
val = Operate.Tms(curve,0.003);
var setcolour=1;
curve.colour = setcolour;
setcolour++;
curve = curve.Next();
while (curve) {
	val = Operate.Tms(curve,0.003);
	curve.colour = setcolour;
	setcolour++;
	if (setcolour > 30) {
		setcolour=1
	}
	curve = curve.Next();
}

DialogueInput("PROPERTIES", "FO", "PRECISION", 1);           // 2 indicates the precision value, i.e., 2 decimal places
DialogueInput("PROPERTIES", "FO", "VALUES", "GE");           // GE for General, AU for Automatic, and SC for Scientific number format
DialogueInput("PROPERTIES", "FO", "FONT", "", "", "CURVE");  // Changing injury text colour to the curve colour

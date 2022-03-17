gpsref_timestatus = {

    "UNKNOWN": "Time validity is unknown",
    "APPROXIMATE": "Time is set approximately",
    "COARSEADJUSTING": "Time is approaching coarse precision",
    "COARSE": "This time is valid to coarse precision",
    "COARSESTEERING": "Time is coarse set and is being steered",
    "FREEWHEELING": "Position is lost and the range bias cannot be calculated",
    "FINEADJUSTING": "Time is adjusting to fine precision",
    "FINE": "Time has fine precision",
    "FINEBACKUPSTEERING": "Time is fine set and is being steered by the backup system",
    "FINESTEERING": "Time is fine set and is being steered",
    "SATTIME": "Time from satellite. Only used in logs containing satellite data such as ephemeris and almanac"

}

recieverstatus = {

    '0x00000001': 'Error flag',
    '0x00000002': 'Temperature status',
    '0x00000004': 'Voltage supply status',
    '0x00000008': 'Primary antenna power status',
    '0x00000010': 'LNA Failure',
    '0x00000020': 'Primary antenna open circuit flag. This flag is only available on certain products.',
    '0x00000040': 'Primary antenna short circuit flag. This flag is only available on certain products.',
    '0x00000080': 'CPU overload flag. This flag is only available on certain products.',
    '0x00000100': 'COM port transmit buffer overrun. ',
    '0x00000200': 'Spoofing Detection Status',
    '0x00000400': 'Reserved',
    '0x00000800': 'Link overrun flag, This flag indicates if any of the USB, ICOM, CCOM, NCOM or File ports are overrun. ',
    '0x00001000': 'Input overrun flag',
    '0x00002000': 'Aux transmit overrun flag',
    '0x00004000': 'Antenna gain state',
    '0x00008000': 'Jammer Detected',
    '0x00010000': 'INS reset flag',
    '0x00020000': 'IMU communication failure',
    '0x00040000': 'GPS almanac flag/UTC known',
    '0x00080000': 'Position solution flag',
    '0x00100000': 'Position fixed flag, see the FIX command',
    '0x00200000': 'Clock steering status',
    '0x00400000': 'Clock model flag',
    '0x00800000': 'External oscillator locked flag',
    '0x01000000': 'Software resource',
    '0x06000000': 'Interpret Status/Error Bits as OEM7 format',
    '0x08000000': 'Tracking mode',
    '0x10000000': 'Digital Filtering Enabled',
    '0x20000000': 'Auxiliary 3 status event flag',
    '0x40000000': 'Auxiliary 2 status event flag',
    '0x80000000': 'Auxiliary 1 status event flag'


}

numberofdatafields = {

    "BESTPOS": 24,
    "BESTGNSSPOS": 24,
    "INSPVAX": 26,
    "RANGE": 13,
    "TRACKSTAT": 18,
    "SATVIS2": 14,
    "HEADING2": 21,
    "PASSTHROUGH": 6,

    "GPSEPHEM": 35,
    "GLOEPHEMERIS": 32,
    "BDSEPHEMERIS": 31,
    "BDSBCNAV1EPHEMERIS": 35,
    "BDSBCNAV2EPHEMERIS": 35,
    "GALINAVEPHEMERIS": 37,
    "GALFNAVEPHEMERIS": 32,
    "QZSSEPHEMERIS": 39,

    "VERSION": 13,
    "RXCONFIG": 6,
    "RXSTATUS": 25,
    "INSCONFIG": 30,
    "INSUPDATESTATUS": 13,
    "CHANCONFIGLIST": 9

}

logtypes = {

    "BESTPOS": "GNSS",
    "BESTGNSSPOS": "SPAN",
    "INSPVAX": "SPAN",
    "RANGE": "GNSS",
    "TRACKSTAT": "GNSS",
    "SATVIS2": "GNSS",
    "RAWIMUSX": "SPAN",
    "HEADING2": "GNSS",
    "PASSTHROUGH": "GNSS",

    "GPSEPHEM": "GNSS",
    "GLOEPHEMERIS": "GNSS",
    "BDSEPHEMERIS": "GNSS",
    "BDSBCNAV1EPHEMERIS": "GNSS",
    "BDSBCNAV2EPHEMERIS": "GNSS",
    "GALINAVEPHEMERIS": "GNSS",
    "GALFNAVEPHEMERIS": "GNSS",
    "QZSSEPHEMERIS": "GNSS",

    "VERSION": "GNSS",
    "RXCONFIG": "GNSS",
    "RXSTATUS": "GNSS",
    "INSCONFIG": "SPAN",
    "INSUPDATESTATUS": "SPAN",
    "CHANCONFIGLIST": "GNSS"

}

bestpos_solutionsstatus = {

    "SOL_COMPUTED": "Solution computed",
    "INSUFFICIENT_OBS": "Insufficient observations",
    "NO_CONVERGENCE": "No convergence",
    "COV_TRACE": "Covariance trace exceeds maximum (trace > 1000 m)",
    "TEST_DIST": "Test distance exceeded (maximum of 3 rejections if distance >10 km)",
    "COLD_START": "Not yet converged from cold start",
    "V_H_LIMIT": "Height or velocity limits exceeded (in accordance with export licensing restrictions)",
    "VARIANCE": "Variance exceeds limits",
    "RESIDUALS": "Residuals are too large",
    "INTEGRITY_WARNING": "Large residuals make position unreliable",
    "INVALID_FIX": "The fixed position, entered using the FIX position command, is not valid",
    "INVALID_RATE": "The selected logging rate is not supported for this solution type."

}

bestpos_posveltype = {
    "NONE": "No solution",
    "FIXEDPOS": "Position has been fixed by the FIX position command or by position averaging.",
    "DOPPLER_VELOCITY":	"Velocity computed using instantaneous Doppler",
    "SINGLE": "Solution calculated using only data supplied by the GNSS satellites",
    "PSRDIFF": "Solution calculated using pseudorange differential(DGPS, DGNSS) corrections",
    "WAAS": "Solution calculated using corrections from an SBAS satellite",
    "PROPAGATED": "Propagated by a Kalman filter without new observations",
    "L1_FLOAT": "Single-frequency RTK solution with unresolved, float carrier phase ambiguities",
    "NARROW_FLOAT": "Multi-frequency RTK solution with unresolved, float carrier phase ambiguities",
    "L1_INT": "Single-frequency RTK solution with carrier phase ambiguities resolved to integers",
    "WIDE_INT": "Multi-frequency RTK solution with carrier phase ambiguities resolved to wide-lane integers",
    "NARROW_INT": "Multi-frequency RTK solution with carrier phase ambiguities resolved to narrow-lane integers",
    "RTK_DIRECT_INS": "RTK status where the RTK filter is directly initialized from the INS filter",
    "INS_SBAS": "INS position, where the last applied position update used a GNSS solution computed using corrections from an SBAS(WAAS) solution",
    "INS_PSRSP": "INS position, where the last applied position update used a single point GNSS(SINGLE) solution",
    "INS_PSRDIFF": "INS position, where the last applied position update used a pseudorange differential GNSS(PSRDIFF) solution",
    "INS_RTKFLOAT": "INS position, where the last applied position update used a floating ambiguity RTK(L1_FLOAT or NARROW_FLOAT) solution",
    "INS_RTKFIXED": "INS position, where the last applied position update used a fixed integer ambiguity RTK(L1_INT, WIDE_INT or NARROW_INT) solution",
    "PPP_CONVERGING": "Converging TerraStar-C, TerraStar-C PRO or TerraStar-X solution",
    "PPP": "Converged TerraStar-C, TerraStar-C PRO or TerraStar-X solution",
    "OPERATIONAL": "Solution accuracy is within UAL operational limit",
    "WARNING": "Solution accuracy is outside UAL operational limit but within warning limit",
    "OUT_OF_BOUNDS": "Solution accuracy is outside UAL limits",
    "INS_PPP_CONVERGING": "INS position, where the last applied position update used a converging TerraStar-C, TerraStar-C PRO or TerraStar-X PPP(PPP_CONVERGING) solution",
    "INS_PPP": "INS position, where the last applied position update used a converged TerraStar-C, TerraStar-C PRO or TerraStar-X PPP(PPP) solution",
    "PPP_BASIC_CONVERGING": "Converging TerraStar-L solution",
    "PPP_BASIC": "Converged TerraStar-L solution",
    "INS_PPP_BASIC_CONVERGING": "INS position, where the last applied position update used a converging TerraStar-L PPP(PPP_BASIC) solution",
    "INS_PPP_BASIC": "INS position, where the last applied position update used a converged TerraStar-L PPP(PPP_BASIC) solution"

}

bestpos_ess = {

    "00":  "Unknown or default Klobuchar model",
    "01": "RTK verified or Glide",
    "02": "SBAS Broadcast",
    "03": " Multi-frequency Computed",
    "04": " PSRDiff Correction",
    "05": "NovAtel Blended Iono Value",
    "06": "Reserved (unsure)",
    "10": "RTK ASSIST active",
    "20": "No antenna warning",
    "21": "Antenna information is missing",
    "80": "Terrain Compensation corrections are not used",
    "81": "Position includes Terrain Compensation corrections"
}

bestpos_galbei_sigmask = {
    "00": "Galileo E1 used in Solution (unsure)",
    "01":  "Galileo E1 used in Solution",
    "02": "Galileo E5a used in Solution",
    "04": "Galileo E5b used in Solution",
    "06": "BeiDou B3 used in Solution (B3I), unsure",
    "08": "Galileo ALTBOC used in Solution",
    "10": "BeiDou B1 used in Solution (B1I and B1C)",
    "20": "BeiDou B2 used in Solution (B2I, B2a and B2b)",
    "40": "BeiDou B3 used in Solution (B3I)",
    "80": "Galileo E6 used in Solution (E6B and E6C)"


}

bestpos_gpsglo_sigmask = {

    "00":  "GPS L1 used in Solution (unsure)",
    "01":  "GPS L1 used in Solution",
    "02": "GPS L2 used in Solution",
    "03": "Reserved (unsure)",
    "11": "unkown",
    "33": "unknown",
    "04": "GPS L5 used in Solution",
    "10": "GLONASS L1 used in Solution",
    "20": "GLONASS L2 used in Solution",
    "40": "GLONASS L3 used in Solution"

}

interial_solution_status = {

    'INS_INACTIVE': 'IMU logs are present, but the alignment routine has not started; INS is inactive.',
    'INS_ALIGNING': 'INS is in alignment mode.',
    'INS_HIGH_VARIANCE': 'The INS solution uncertainty contains outliers and the solution may be outside specifications.1 The solution is still valid but you should monitor the solution uncertainty in the INSSTDEV log. It may be encountered during times when GNSS is absent or poor.',
    'INS_SOLUTION_GOOD': 'The INS filter is in navigation mode and the INS solution is good.',
    'INS_SOLUTION_FREE': 'The INS Filter is in navigation mode and the GNSS solution is suspected to be in error. The inertial filter will report this status when there are no available updates (GNSS or other) being accepted and used.',
    'INS_ALIGNMENT_COMPLETE': 'The INS filter is in navigation mode, but not enough vehicle dynamics have been experienced for the system to be within specifications.',
    'DETERMINING_ORIENTATION': 'INS is determining the IMU axis aligned with gravity.',
    'WAITING_INITIALPOS': 'The INS filter has determined the IMU orientation and is awaiting an initial position estimate to begin the alignment process.',
    'WAITING_AZIMUTH': 'The INS filer has orientation, initial biases, initial position and valid roll/pitch estimated. Will not proceed until initial azimuth is entered.',
    'INITIALIZING_BIASES': 'The INS filter is estimating initial biases during the first 10 seconds of stationary data.',
    'MOTION_DETECT': 'The INS filter has not completely aligned, but has detected motion.',
    'WAITING_ALIGNMENTORIENTATION': 'The INS filter is waiting to start alignment until the current Vehicle Frame roll and pitch estimates are within the configured threshold of the expected orientation (set by the SETALIGNMENTORIENTATION command).'


}
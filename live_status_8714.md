JWST Program 8714 — Live Status Log

## Program Summary
- **Program**: 8714 — Cold Jupiter isotopes
- **Status**: Flight Ready (awaiting visit executions)
- **EAP**: 12 months from each visit completion
- **Monitoring**: Real-time tracking via Space Telescope Live
- **Primary Target**: Cold Jupiter atmospheric composition analysis

## Visit Execution Tracking

### Status Categories
- **Scheduled**: Visit planned and scheduled in queue
- **Executing**: Currently observing
- **Complete**: Data acquired and available
- **Failed**: Observation failed (requires rescheduling)
- **Partial**: Partial data acquired (may need completion)

### Data Entry Format
Status table entries (append as visits execute):
- **Columns**: date_utc | obsid | instrument | mode | state | t_exp | dithers | notes

### Live Status Log

**Current Status Data:**
- 2025-09-03T21:22:07Z | 01K3PCDBN6HJ1V5DHBSPT8BGS8 | (TBD) | (TBD) | Scheduled | (TBD) | (TBD) | Initial placeholder

### Usage Instructions

#### Manual Updates
To add new entries manually, append lines in the format above to this file.

#### Automated Updates
Use the GitHub Actions workflow:
1. Go to GitHub → Actions
2. Select "Append JWST status entry" workflow
3. Fill in required parameters
4. Run workflow to automatically append entry

#### Quality Control
- Verify observation IDs against Space Telescope Live
- Cross-check execution times with planned schedules  
- Note any anomalies or deviations from expected parameters
- Update status as visits progress through execution phases

### Data Processing Notes
- Initial data products available ~24-48 hours post-execution
- Full pipeline products available within ~1 week
- Proprietary period: 12 months from visit completion
- Archive location: MAST (Barbara A. Mikulski Archive for Space Telescopes)

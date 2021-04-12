 -- to get all resumes against the job
select * from ps_hrs_Rcmnt where hrs_job_opening_id = '19376';

----------------------------------------------------------------------------------
-- resume queries
select * from ps_hrs_app_profile where hrs_person_id = '243936'  and hrs_profile_seq='1';

select * from PS_HRS_APP_RES where hrs_resume_id = '195425';



-- file seq to be considered as maximum for now(assumption)
SELECT FILE_DATA, FILE_SIZE
FROM PS_HRS_ATTACHMENTS
WHERE ATTACHSYSFILENAME = 'Apr172019061735resume.pdf';



select * from  PS_HRS_ATTACHMENTS
WHERE ATTACHSYSFILENAME = 'Apr172019061735resume.pdf';
-----------------------------------------------------------------------------------

-- details about applicant
select J_FUNCTIONAL_AREA, --functional area,
    J_INDUSTRY, --industry,
    J_GRADUATION,  --educational details,
    J_POST_GRAD,    --pg details
    J_EXP_YEAR, -- experience year
    J_EXP_MONTH --experience month
from PS_J_HRS_APP_COSTM where hrs_person_id = '341973' ;


-- gender query
select sex from PS_HRS_APPLICANT where hrs_person_id = '341973';


-- notice period (value to be provided)
select J_NOTICE_PERIOD from ps_hrs_app_profile  where hrs_person_id = '243936' and hrs_profile_seq='1';
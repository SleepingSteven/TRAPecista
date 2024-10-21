examples=[{
        "input": "Provide a query to retrieve all the quenches",
        "query": """SELECT * 
          FROM (SELECT      a.CIRCUIT_ID, a.TESTPLAN_ACTIVITY_RES_ID,      e.ASSEMBLY_ID,      c.ARCHETYPE_ID,      c.ARCHETYPE_OUTPUT_NAME,      c.ARCHETYPE_OUTPUT_UNIT,      c.ARCHETYPE_OUTPUT_ORDER,      a.TESTPLAN_ACT_RES_OUT_VALUE,      b.TESTPLAN_ACTIVITY_RES_DATE,     b.STEP_ACTIVITY_ID,     b.TESTPLAN_ID,     b.TESTPLAN_ACTIVITY_CYCLE FROM CVG_TESTPLAN_ACTIVITY_RES_OUT a LEFT JOIN CVG_TESTPLAN_ACTIVITY_RES b ON a.TESTPLAN_ACTIVITY_RES_ID=b.TESTPLAN_ACTIVITY_RES_ID LEFT JOIN CVG_ARCHETYPE_OUTPUT c ON a.ARCHETYPE_OUTPUT_ID=c.ARCHETYPE_OUTPUT_ID LEFT JOIN CVG_TESTPLAN d ON b.TESTPLAN_ID=d.TESTPLAN_ID LEFT JOIN CVG_ASSEMBLY_SETUP e ON d.ASSEMBLY_SETUP_ID=e.ASSEMBLY_SETUP_ID)
          WHERE ARCHETYPE_ID IN (4,5)
          AND (
          ARCHETYPE_OUTPUT_NAME LIKE 'Temperature' OR
          ARCHETYPE_OUTPUT_NAME LIKE '%Ramp rate%' OR
          ARCHETYPE_OUTPUT_NAME LIKE 'dI/dt (t < 0)' OR
          ARCHETYPE_OUTPUT_NAME LIKE 'Current' OR
          ARCHETYPE_OUTPUT_NAME LIKE 'Trigger Type' OR
          ARCHETYPE_OUTPUT_NAME LIKE 'File name' OR
          ARCHETYPE_OUTPUT_NAME LIKE 'Quench File' OR
          ARCHETYPE_OUTPUT_NAME LIKE 'Q.Seg Name'
          )"""
    },
    {
        "input": "Provide a query to retrieve all the natural quenches at 1.9 K temperature and dI/dt (before 0) between 10 and 30 (A/s)",
        "query": """SELECT a.CIRCUIT_ID, a.TESTPLAN_ACTIVITY_RES_ID,
       e.ASSEMBLY_ID, c.ARCHETYPE_ID, c.ARCHETYPE_OUTPUT_NAME,
       c.ARCHETYPE_OUTPUT_UNIT, c.ARCHETYPE_OUTPUT_ORDER,
       a.TESTPLAN_ACT_RES_OUT_VALUE, b.TESTPLAN_ACTIVITY_RES_DATE,
       b.STEP_ACTIVITY_ID, b.TESTPLAN_ID, b.TESTPLAN_ACTIVITY_CYCLE
FROM CVG_TESTPLAN_ACTIVITY_RES_OUT a
LEFT JOIN CVG_TESTPLAN_ACTIVITY_RES b ON a.TESTPLAN_ACTIVITY_RES_ID = b.TESTPLAN_ACTIVITY_RES_ID
LEFT JOIN CVG_ARCHETYPE_OUTPUT c ON a.ARCHETYPE_OUTPUT_ID = c.ARCHETYPE_OUTPUT_ID
LEFT JOIN CVG_TESTPLAN d ON b.TESTPLAN_ID = d.TESTPLAN_ID
LEFT JOIN CVG_ASSEMBLY_SETUP e ON d.ASSEMBLY_SETUP_ID = e.ASSEMBLY_SETUP_ID
WHERE ARCHETYPE_ID IN (4,5)
AND (
    (ARCHETYPE_OUTPUT_NAME LIKE 'Temperature' AND a.TESTPLAN_ACT_RES_OUT_VALUE = '1.9') OR
    (ARCHETYPE_OUTPUT_NAME LIKE 'dI/dt (t < 0)' AND a.TESTPLAN_ACT_RES_OUT_VALUE BETWEEN '10' AND '30') OR
    (ARCHETYPE_OUTPUT_NAME LIKE 'Trigger Type' AND a.TESTPLAN_ACT_RES_OUT_VALUE = 'Natural quench')
)"""
    },
    {
        "input": "Provide a query to get all the results for the testplan n.1141",
        "query": """SELECT     a.CIRCUIT_ID, j.CIRCUIT_NAME, a.TESTPLAN_ACTIVITY_RES_ID,     e.ASSEMBLY_ID,     c.ARCHETYPE_ID,     c.ARCHETYPE_OUTPUT_NAME,     c.ARCHETYPE_OUTPUT_UNIT,     c.ARCHETYPE_OUTPUT_ORDER,     a.TESTPLAN_ACT_RES_OUT_VALUE,     a.TESTPLAN_ACT_RES_OUT_GROUP,     b.TESTPLAN_ACTIVITY_RES_DATE,     b.TESTPLAN_ACTIVITY_RES_COM,     b.STEP_ACTIVITY_ID,     f.STEP_ACTIVITY_NAME,     b.TESTPLAN_ID,     b.TESTPLAN_ACTIVITY_CYCLE,     b.USER_ID_ACTIVITY_RES,     CONCAT(CONCAT(TRIM(h.USER_FNAME), ' '), TRIM(h.USER_SNAME)) AS USER_NAME_ACTIVITY_RES,     b.USER_ID_ACTIVITY_RES_APT,     CONCAT(CONCAT(TRIM(i.USER_FNAME), ' '), TRIM(i.USER_SNAME)) AS USER_NAME_ACTIVITY_RES_APT,     g.STEP_ID,     g.STEP_NAME,     g.STEP_TEMP FROM CVG_TESTPLAN_ACTIVITY_RES_OUT a LEFT JOIN CVG_TESTPLAN_ACTIVITY_RES b ON a.TESTPLAN_ACTIVITY_RES_ID=b.TESTPLAN_ACTIVITY_RES_ID LEFT JOIN CVG_ARCHETYPE_OUTPUT c ON a.ARCHETYPE_OUTPUT_ID=c.ARCHETYPE_OUTPUT_ID LEFT JOIN CVG_TESTPLAN d ON b.TESTPLAN_ID=d.TESTPLAN_ID LEFT JOIN CVG_ASSEMBLY_SETUP e ON d.ASSEMBLY_SETUP_ID=e.ASSEMBLY_SETUP_ID LEFT JOIN CVG_STEP_ACTIVITY f ON b.STEP_ACTIVITY_ID=f.STEP_ACTIVITY_ID LEFT JOIN CVG_STEP g ON f.STEP_ID=g.STEP_ID LEFT JOIN CVG_USER h ON b.USER_ID_ACTIVITY_RES=h.USER_ID LEFT JOIN CVG_USER i ON b.USER_ID_ACTIVITY_RES_APT=i.USER_ID LEFT JOIN CVG_CIRCUIT j ON j.CIRCUIT_ID = a.CIRCUIT_ID
where b.testplan_id=1141"""
    },
    {
        "input": "Provide a query to get all the item attributes for the testplan n.1141",
        "query": """SELECT b.CIRCUIT_ATTR_NAME, a.CIRCUIT_ATTR_SETUP_VALUE, a.CIRCUIT_ID, f.CIRCUIT_NAME, ci.ITEM_ID, c.ASSEMBLY_ID, e.TESTPLAN_ID FROM CVG_CIRCUIT_ATTR_SETUP a LEFT JOIN CVG_CIRCUIT_ATTR b ON a.CIRCUIT_ATTR_ID=b.CIRCUIT_ATTR_ID LEFT JOIN CVG_CIRCUIT_ITEM ci ON ci.CIRCUIT_ID=a.CIRCUIT_ID LEFT JOIN CVG_CIRCUIT f ON f.CIRCUIT_ID=a.CIRCUIT_ID LEFT JOIN CVG_ASSEMBLY_CONFIG c ON c.ITEM_ID=ci.ITEM_ID LEFT JOIN CVG_ASSEMBLY_SETUP d ON c.ASSEMBLY_ID=d.ASSEMBLY_ID LEFT JOIN CVG_TESTPLAN e ON d.ASSEMBLY_SETUP_ID = e.ASSEMBLY_SETUP_ID
where e.testplan_id=1141"""
    },
    {
        "input": "Provide a query to retrive all the HV tests results of the testplan n.1141",
        "query": """SELECT     a.CIRCUIT_ID, j.CIRCUIT_NAME, a.TESTPLAN_ACTIVITY_RES_ID,     e.ASSEMBLY_ID,     c.ARCHETYPE_ID,     c.ARCHETYPE_OUTPUT_NAME,     c.ARCHETYPE_OUTPUT_UNIT,     c.ARCHETYPE_OUTPUT_ORDER,     a.TESTPLAN_ACT_RES_OUT_VALUE,     a.TESTPLAN_ACT_RES_OUT_GROUP,     b.TESTPLAN_ACTIVITY_RES_DATE,     b.TESTPLAN_ACTIVITY_RES_COM,     b.STEP_ACTIVITY_ID,     f.STEP_ACTIVITY_NAME,     b.TESTPLAN_ID,     b.TESTPLAN_ACTIVITY_CYCLE,     b.USER_ID_ACTIVITY_RES,     CONCAT(CONCAT(TRIM(h.USER_FNAME), ' '), TRIM(h.USER_SNAME)) AS USER_NAME_ACTIVITY_RES,     b.USER_ID_ACTIVITY_RES_APT,     CONCAT(CONCAT(TRIM(i.USER_FNAME), ' '), TRIM(i.USER_SNAME)) AS USER_NAME_ACTIVITY_RES_APT,     g.STEP_ID,     g.STEP_NAME,     g.STEP_TEMP FROM CVG_TESTPLAN_ACTIVITY_RES_OUT a LEFT JOIN CVG_TESTPLAN_ACTIVITY_RES b ON a.TESTPLAN_ACTIVITY_RES_ID=b.TESTPLAN_ACTIVITY_RES_ID LEFT JOIN CVG_ARCHETYPE_OUTPUT c ON a.ARCHETYPE_OUTPUT_ID=c.ARCHETYPE_OUTPUT_ID LEFT JOIN CVG_TESTPLAN d ON b.TESTPLAN_ID=d.TESTPLAN_ID LEFT JOIN CVG_ASSEMBLY_SETUP e ON d.ASSEMBLY_SETUP_ID=e.ASSEMBLY_SETUP_ID LEFT JOIN CVG_STEP_ACTIVITY f ON b.STEP_ACTIVITY_ID=f.STEP_ACTIVITY_ID LEFT JOIN CVG_STEP g ON f.STEP_ID=g.STEP_ID LEFT JOIN CVG_USER h ON b.USER_ID_ACTIVITY_RES=h.USER_ID LEFT JOIN CVG_USER i ON b.USER_ID_ACTIVITY_RES_APT=i.USER_ID LEFT JOIN CVG_CIRCUIT j ON j.CIRCUIT_ID = a.CIRCUIT_ID
where c.ARCHETYPE_ID=1 and b.testplan_id=1141
ORDER BY TESTPLAN_ACTIVITY_RES_DATE ASC, TESTPLAN_ACTIVITY_RES_ID ASC, ARCHETYPE_OUTPUT_NAME ASC, TESTPLAN_ACT_RES_OUT_GROUP ASC"""
    },
    {
        "input": "Provide a query to retrieve the information useful for investigating quenches detection times for testplan 1141",
        "query":"""SELECT * 
FROM (SELECT     a.TESTPLAN_ACTIVITY_RES_ID,     e.ASSEMBLY_ID,     c.ARCHETYPE_ID,     c.ARCHETYPE_OUTPUT_NAME,     c.ARCHETYPE_OUTPUT_UNIT,     c.ARCHETYPE_OUTPUT_ORDER,     a.TESTPLAN_ACT_RES_OUT_VALUE,     a.TESTPLAN_ACT_RES_OUT_GROUP,     b.TESTPLAN_ACTIVITY_RES_DATE,     b.STEP_ACTIVITY_ID,     b.TESTPLAN_ID,     b.TESTPLAN_ACTIVITY_CYCLE FROM CVG_TESTPLAN_ACTIVITY_RES_OUT a LEFT JOIN CVG_TESTPLAN_ACTIVITY_RES b ON a.TESTPLAN_ACTIVITY_RES_ID=b.TESTPLAN_ACTIVITY_RES_ID LEFT JOIN CVG_ARCHETYPE_OUTPUT c ON a.ARCHETYPE_OUTPUT_ID=c.ARCHETYPE_OUTPUT_ID LEFT JOIN CVG_TESTPLAN d ON b.TESTPLAN_ID=d.TESTPLAN_ID LEFT JOIN CVG_ASSEMBLY_SETUP e ON d.ASSEMBLY_SETUP_ID=e.ASSEMBLY_SETUP_ID) 
WHERE TESTPLAN_ID=1141
AND ARCHETYPE_ID IN (4) 
AND (
ARCHETYPE_OUTPUT_NAME LIKE 'Temperature' OR 
ARCHETYPE_OUTPUT_NAME LIKE '%Ramp rate%' OR 
ARCHETYPE_OUTPUT_NAME LIKE 'dI/dt (t < 0)' OR 
ARCHETYPE_OUTPUT_NAME LIKE 'Current' OR 
ARCHETYPE_OUTPUT_NAME LIKE 'Trigger Type' OR 
ARCHETYPE_OUTPUT_NAME LIKE 'File name' OR 
ARCHETYPE_OUTPUT_NAME LIKE 'Quench File' OR 
ARCHETYPE_OUTPUT_NAME LIKE 'Q.Det Name' OR 
ARCHETYPE_OUTPUT_NAME LIKE 'Q.Det Voltage' OR 
ARCHETYPE_OUTPUT_NAME LIKE 'Q.Det Time' OR 
ARCHETYPE_OUTPUT_NAME LIKE 'Q.Seg Name'
)
ORDER BY TESTPLAN_ACTIVITY_RES_DATE ASC, TESTPLAN_ACTIVITY_RES_ID ASC """
    },
    {
        "input": "Provide a query for obtaining the most recent test results that have a specific status (OK) and were authored by a particular user group (TE-MSC-TM)",
        "query": """SELECT a.TESTPLAN_ACTIVITY_RES_ID, 
       a.TESTPLAN_ACTIVITY_RES_DATE, 
       c.ARCHETYPE_OUTPUT_NAME, 
       b.TESTPLAN_ACT_RES_OUT_VALUE
FROM CVG_TESTPLAN_ACTIVITY_RES a
JOIN CVG_TESTPLAN_ACTIVITY_RES_OUT b ON a.TESTPLAN_ACTIVITY_RES_ID = b.TESTPLAN_ACTIVITY_RES_ID
JOIN CVG_ARCHETYPE_OUTPUT c ON b.ARCHETYPE_OUTPUT_ID = c.ARCHETYPE_OUTPUT_ID
WHERE a.TESTPLAN_ID IN (
    SELECT TESTPLAN_ID 
    FROM CVG_TESTPLAN 
    WHERE user_id_testplan_author IN (
        SELECT user_id 
        FROM CVG_USER 
        WHERE user_group = 'TE-MSC-TM'
    )
) AND b.TESTPLAN_ACT_RES_OUT_VALUE IN (
    SELECT TESTPLAN_ACT_RES_OUT_VALUE 
    FROM CVG_TESTPLAN_ACTIVITY_RES 
    WHERE TESTPLAN_ACTIVITY_RES_STS_ID = 9
)
ORDER BY a.TESTPLAN_ACTIVITY_RES_DATE DESC
FETCH FIRST 10 ROWS ONLY;"""},
    {
        "input": "Provide a query that retrieves detailed information about the most recent activities, along with their results, for a specific test plan (1582)",
        "query": """SELECT 
    tp.testplan_id,
    tp.testplan_date,
    tp.testplan_com,
    tp.user_id_testplan_author,
    tp.user_id_testplan_engineer,
    tp.user_id_testplan_operator,
    tp.insert_setup_id,
    tp.assembly_setup_id,
    sa.step_id,
    sa.step_activity_id,
    sa.step_activity_name,
    sa.step_activity_order,
    sa.step_activity_priority,
    sar.testplan_activity_res_id,
    sar.testplan_activity_res_date,
    sar.user_id_activity_res,
    sar.testplan_activity_res_sts_id,
    sar.testplan_activity_res_com,
    sar.testplan_activity_cycle,
    sao.testplan_act_res_out_value,
    ao.archetype_output_name,
    ao.archetype_output_unit,
    ao.archetype_output_order
FROM 
    cvg_testplan tp
JOIN 
    cvg_testplan_activity ta ON tp.testplan_id = ta.testplan_id
JOIN 
    cvg_step_activity sa ON ta.step_activity_id = sa.step_activity_id
JOIN 
    cvg_testplan_activity_res sar ON ta.testplan_id = sar.testplan_id AND ta.step_activity_id = sar.step_activity_id
JOIN 
    cvg_testplan_activity_res_out sao ON sar.testplan_activity_res_id = sao.testplan_activity_res_id
JOIN 
    cvg_archetype_output ao ON sao.archetype_output_id = ao.archetype_output_id
WHERE 
    tp.testplan_id = 1582   
ORDER BY 
    sar.testplan_activity_res_date DESC
FETCH FIRST 10 ROWS ONLY;"""
    },
    {
        "input": "Provide a query that retrieves all testplans performed in 2022",
        "query": """SELECT 
    testplan_id, 
    testplan_date, 
    user_id_testplan_author, 
    insert_setup_id, 
    assembly_setup_id, 
    user_id_testplan_engineer, 
    user_id_testplan_operator, 
    testplan_edms, 
    testplan_com, 
    testplan_recipe 
FROM 
    cvg_testplan 
WHERE 
    EXTRACT(YEAR FROM testplan_date) = 2022;"""
    },
    {
        "input": "Provide a query that retrieves all activities for a given step name",   
        "query": """SELECT
    sa.step_activity_id,
    sa.step_activity_name,
    sa.step_activity_order,
    sa.step_activity_priority,
    sa.step_activity_duration,
    sa.step_activity_desc,
    sa.step_activity_edms,
    sa.step_activity_sname,
    sa.step_activity_priority_tc,
    sa.step_activity_result_type,
    sa.step_activity_notif_recipient,
    sa.archetype_id,
    sa.user_privilege_id,
    sa.step_activity_option,
    sa.assembly_eqp_id
FROM
    cvg_step s
JOIN
    cvg_step_activity sa ON s.step_id = sa.step_id
WHERE
    s.step_name = 'step name'
ORDER BY
    sa.step_activity_order ASC"""
    },
    {
        "input": "Provide a query that retrieves all circuits used in multi-item assemblies",   
        "query": """SELECT DISTINCT c.circuit_id, c.circuit_name
FROM cvg_circuit c
JOIN cvg_circuit_item ci ON c.circuit_id = ci.circuit_id
JOIN cvg_assembly_config ac ON ci.item_id = ac.item_id
GROUP BY c.circuit_id, c.circuit_name
HAVING COUNT(DISTINCT ac.assembly_id) > 1
"""
    },
    {
        "input": "to retrieve all activities carried out by a member of the TE-MSC-TM unit please",
        "query": """SELECT 
    sa.step_activity_id, 
    sa.step_activity_name, 
    sa.step_activity_order, 
    ta.testplan_id
FROM 
    cvg_testplan_activity ta
JOIN 
    cvg_step_activity sa ON ta.step_activity_id = sa.step_activity_id
JOIN 
    cvg_testplan tp ON ta.testplan_id = tp.testplan_id
WHERE 
    tp.user_id_testplan_engineer IN (
        SELECT user_id 
        FROM cvg_user 
        WHERE user_group = 'TE-MSC-TM'
    )
ORDER BY 
    ta.testplan_id, 
    sa.step_activity_order
FETCH FIRST 10 ROWS ONLY;"""
    },
    {
        "input": "provide a query to retrieve all vertical magnet assemblies",
        "query": """SELECT a.assembly_id, a.assembly_name 
FROM cvg_assembly a 
JOIN cvg_assembly_setup asu ON a.assembly_id = asu.assembly_id 
JOIN cvg_assembly_types at ON a.assembly_type_id = at.assembly_type_id 
WHERE at.assembly_type_name = 'vertical magnet'"""
    },
    {
        "input": "provide a query to retrieve an overview of test plans created within a specific date range (2021/01/01 - 2022/12/12), showing their details, the activities conducted, the results of those activities, and who was responsible for the test plans, with a count of results for each test plan.",
        "query": """SELECT 
    tp.testplan_id,
    tp.testplan_date,
    tp.testplan_com,
    u.user_fname || ' ' || u.user_sname AS engineer_name,
    sa.step_activity_name,
    sar.testplan_activity_res_date,
    sar.testplan_activity_res_com,
    c.circuit_name,
    s.step_name,
    s.step_desc,
    COUNT(sar.testplan_activity_res_id) OVER (PARTITION BY tp.testplan_id) AS total_results
FROM 
    cvg_testplan tp
JOIN 
    cvg_testplan_activity ta ON tp.testplan_id = ta.testplan_id
JOIN 
    cvg_step_activity sa ON ta.step_activity_id = sa.step_activity_id
JOIN 
    cvg_testplan_activity_res sar ON ta.testplan_id = sar.testplan_id AND ta.step_activity_id = sar.step_activity_id
JOIN 
    cvg_circuit c ON c.circuit_id = sa.step_id
JOIN 
    cvg_user u ON tp.user_id_testplan_engineer = u.user_id
JOIN 
    cvg_step s ON sa.step_id = s.step_id
WHERE 
    sar.testplan_activity_res_sts_id IN (9, 10) -- OK and Review
AND 
    tp.testplan_date BETWEEN TO_DATE('2021-01-01', 'YYYY-MM-DD') AND TO_DATE('2022-12-12', 'YYYY-MM-DD')
ORDER BY 
    tp.testplan_date DESC, engineer_name;"""
    },
    {
        "input": "provide a query to retrieve all HV tests for circuits that start with MCBX", 
        "query": """SELECT     a.CIRCUIT_ID, j.CIRCUIT_NAME, a.TESTPLAN_ACTIVITY_RES_ID,     
           e.ASSEMBLY_ID, c.ARCHETYPE_ID, c.ARCHETYPE_OUTPUT_NAME,     
           c.ARCHETYPE_OUTPUT_UNIT, c.ARCHETYPE_OUTPUT_ORDER,     
           a.TESTPLAN_ACT_RES_OUT_VALUE, a.TESTPLAN_ACT_RES_OUT_GROUP,     
           b.TESTPLAN_ACTIVITY_RES_DATE, b.TESTPLAN_ACTIVITY_RES_COM,     
           b.STEP_ACTIVITY_ID, f.STEP_ACTIVITY_NAME, b.TESTPLAN_ID,     
           b.TESTPLAN_ACTIVITY_CYCLE, b.USER_ID_ACTIVITY_RES,     
           CONCAT(CONCAT(TRIM(h.USER_FNAME), ' '), TRIM(h.USER_SNAME)) AS USER_NAME_ACTIVITY_RES,     
           b.USER_ID_ACTIVITY_RES_APT,     
           CONCAT(CONCAT(TRIM(i.USER_FNAME), ' '), TRIM(i.USER_SNAME)) AS USER_NAME_ACTIVITY_RES_APT,     
           g.STEP_ID, g.STEP_NAME, g.STEP_TEMP 
FROM CVG_TESTPLAN_ACTIVITY_RES_OUT a 
LEFT JOIN CVG_TESTPLAN_ACTIVITY_RES b ON a.TESTPLAN_ACTIVITY_RES_ID=b.TESTPLAN_ACTIVITY_RES_ID 
LEFT JOIN CVG_ARCHETYPE_OUTPUT c ON a.ARCHETYPE_OUTPUT_ID=c.ARCHETYPE_OUTPUT_ID 
LEFT JOIN CVG_TESTPLAN d ON b.TESTPLAN_ID=d.TESTPLAN_ID 
LEFT JOIN CVG_ASSEMBLY_SETUP e ON d.ASSEMBLY_SETUP_ID=e.ASSEMBLY_SETUP_ID 
LEFT JOIN CVG_STEP_ACTIVITY f ON b.STEP_ACTIVITY_ID=f.STEP_ACTIVITY_ID 
LEFT JOIN CVG_STEP g ON f.STEP_ID=g.STEP_ID 
LEFT JOIN CVG_USER h ON b.USER_ID_ACTIVITY_RES=h.USER_ID 
LEFT JOIN CVG_USER i ON b.USER_ID_ACTIVITY_RES_APT=i.USER_ID 
LEFT JOIN CVG_CIRCUIT j ON j.CIRCUIT_ID = a.CIRCUIT_ID 
WHERE j.CIRCUIT_NAME LIKE 'MCBX%' AND c.ARCHETYPE_ID=1 
ORDER BY b.TESTPLAN_ACTIVITY_RES_DATE ASC, b.TESTPLAN_ACTIVITY_RES_ID ASC, c.ARCHETYPE_OUTPUT_NAME ASC, a.TESTPLAN_ACT_RES_OUT_GROUP ASC"""
    },
    {
        "input": "Provide a query to retrieve for every hv test performed on magnets that start with MCBX the ambient humidity and the test date. (This is a very important example because it shows how the relationships between some of the main tables work when deqaling with HV tests (archetype, archetype_output, activity_results, activity_results_output, circuit, testplan))",
        "query": """
WITH hv_test_archetype AS (
    SELECT ARCHETYPE_ID
    FROM cvg_archetype
    WHERE archetype_name = 'HV test'
)

SELECT b.TESTPLAN_ACTIVITY_RES_DATE, a.TESTPLAN_ACT_RES_OUT_VALUE
FROM cvg_testplan_activity_res_out a
JOIN cvg_testplan_activity_res b ON a.TESTPLAN_ACTIVITY_RES_ID = b.TESTPLAN_ACTIVITY_RES_ID
JOIN cvg_archetype_output e ON a.ARCHETYPE_OUTPUT_ID = e.ARCHETYPE_OUTPUT_ID
WHERE b.TESTPLAN_ACTIVITY_RES_ID IN (
    SELECT DISTINCT a1.TESTPLAN_ACTIVITY_RES_ID
    FROM cvg_testplan_activity_res_out a1
    JOIN cvg_circuit d ON a1.CIRCUIT_ID = d.CIRCUIT_ID
    WHERE d.CIRCUIT_NAME LIKE 'MCBX%'
)
AND e.ARCHETYPE_OUTPUT_NAME = 'Ambient Humidity'
AND e.ARCHETYPE_ID = (SELECT ARCHETYPE_ID FROM hv_test_archetype)
ORDER BY b.TESTPLAN_ACTIVITY_RES_DATE ASC;

"""
    },
    {
        "input": "Provide a query to retrieve for all quenches for magnets that start with MCB the trigger type (this is a very important example because it shows how the relationship between items, assemblies and testplans work. When dealing with quenches it is very important)",
        "query": """WITH mcb_items AS (
    SELECT item_id
    FROM cvg_item
    WHERE item_name LIKE 'MCB%'
),

assembly_items AS (
    SELECT DISTINCT ac.assembly_id
    FROM cvg_assembly_config ac
    WHERE ac.item_id IN (SELECT item_id FROM mcb_items)
)

SELECT DISTINCT  -- Using DISTINCT to remove duplicates
    t.testplan_id,  
    e.testplan_activity_res_id,  
    e.testplan_act_res_out_value AS trigger_type  
FROM 
    cvg_testplan_activity_res_out e
JOIN 
    cvg_testplan_activity_res b ON e.testplan_activity_res_id = b.testplan_activity_res_id
JOIN 
    cvg_testplan_activity ta ON b.testplan_id = ta.testplan_id
JOIN 
    cvg_testplan t ON ta.testplan_id = t.testplan_id
JOIN 
    cvg_assembly_setup asu ON t.assembly_setup_id = asu.assembly_setup_id
WHERE 
    asu.assembly_id IN (SELECT assembly_id FROM assembly_items) AND
    EXISTS (
        SELECT 1
        FROM cvg_archetype_output ao
        JOIN cvg_archetype a ON ao.archetype_id = a.archetype_id
        WHERE e.archetype_output_id = ao.archetype_output_id AND
              a.archetype_name = 'Quench' AND
              ao.archetype_output_name = 'Trigger Type'
    );"""
    }
    ]

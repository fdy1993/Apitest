INSERT INTO interface_test.`case` (id, app, module, title, method, url, run, headers, pre_case_id, pre_fields, request_body, expect_result, assert_type, pass, msg, update_time, response) VALUES (1, 'ErgoSportive', '登录&注册', '用户登录接口', 'post', '/user/account/login', 'yes', '{"Content-Type": "application/json"}', -1, '[]', '{"platform": "iOS","email": "fandy@keeson.com","password": "753014306"}', '1000', 'code', 'True', '模块:登录&注册, 标题:用户登录接口,断⾔言类型:code,响应:SUCCESS', '2021-11-22 16:17:15', '');
INSERT INTO interface_test.`case` (id, app, module, title, method, url, run, headers, pre_case_id, pre_fields, request_body, expect_result, assert_type, pass, msg, update_time, response) VALUES (2, 'ErgoSportive', '获取设备信息', '获取设备信息', 'post', '/device/getBedInfo', 'yes', '{"Content-Type": "application/json","token":"$token$"}', 1, '[{"field":"token","scope":"header"},{"field":"user_id","scope":"body"}]', '{"user_id": "$user_id$"}', '1000', 'code', 'True', '模块:获取设备信息, 标题:获取设备信息,断⾔言类型:code,响应:SUCCESS', '2021-11-22 16:17:16', '');
-- SELECT * FROM django_migrations;
-- delete from django_migrations where id=22

SELECT * FROM levelupapi_gametype;
SELECT * FROM auth_user;
SELECT * FROM authtoken_token;
SELECT * FROM levelupapi_gamer;
SELECT * FROM levelupapi_status;
SELECT * FROM levelupapi_game;
SELECT * FROM levelupapi_event;


update levelupapi_event
set time = 'joyce@nss.com'
where id = 2;

delete from levelupapi_event
where id = 12;





--select rq.id, rq.keywords from hh_requests rq
--insert into hh_requests (keywords) VALUES ("NAME:(Python)")
--select rs.skill_name, rs.skill_count, rs.skill_persent from hh_responses rs where rs.requests_id = 1 order by rs.skill_count desc
--insert into hh_responses (requests_id, skill_name, skill_count, skill_persent) VALUES (1, "python", 16, 27)
--insert into hh_responses (requests_id, skill_name, skill_count, skill_persent) VALUES (1, "django", 7, 12)

-- select max(rq.id) from hh_requests rq
-- select rq.keywords from hh_requests rq where rq.id = 2
-- select rs.skill_name, rs.skill_count, rs.skill_persent from hh_responses rs where rs.requests_id = 2 order by rs.skill_count desc
-- migrate:up
create table ranks (
    id serial not null primary key,
    name varchar(100) not null,
    enabled boolean not null default true,
    rank_category_id int not null
);

-- migrate:down
drop table ranks;

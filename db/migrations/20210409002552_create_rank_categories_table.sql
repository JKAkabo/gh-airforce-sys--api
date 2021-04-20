-- migrate:up
create table rank_categories (
    id serial not null primary key,
    name varchar(100) not null,
    enabled boolean not null default true
);

-- migrate:down
drop table rank_categories;

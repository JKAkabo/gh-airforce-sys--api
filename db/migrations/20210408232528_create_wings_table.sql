-- migrate:up
create table wings (
    id serial not null primary key,
    name varchar(100) not null,
    enabled boolean not null default true
);

-- migrate:down
drop table wings;
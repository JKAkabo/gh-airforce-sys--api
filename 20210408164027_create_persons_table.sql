-- migrate:up
create table persons (
    id serial not null primary key,
    first_name varchar(100),
    last_name varchar(100),
    email varchar(255) not null,
    phone varchar(10),
    password varchar(60),
    is_superuser boolean not null default false,
    disabled boolean not null default false,
    can_login boolean not null default false,
    created_at timestamp not null,
    updated_at timestamp,
    deleted_at timestamp
);

-- migrate:down
drop table persons;
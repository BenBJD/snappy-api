import pool from "./connection.js"
let sql = `create table if not exists "user"
(
    id             uuid    default gen_random_uuid() not null
        primary key,
    username       text                              not null,
    "passwordHash" text                              not null,
    "snappyScore"  integer default 0                 not null,
    "loginToken"   uuid
);

create table if not exists snap
(
    id           uuid    default gen_random_uuid() not null
        primary key,
    "fromUserId" uuid                              not null
        references "user",
    "toUserId"   uuid                              not null
        references "user",
    date         date    default CURRENT_DATE      not null,
    time         time(0) default CURRENT_TIME      not null,
    seen         boolean default false             not null
);

create table if not exists friend
(
    "user1Id" uuid                  not null
        references "user",
    "user2Id" uuid                  not null
        references "user",
    confirmed boolean default false not null
);

`
export default async () => await pool.query(sql)

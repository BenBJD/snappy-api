import pool from "./connection.js"

export const createRequest = async (user1Id, user2Id) => {
  const res = await pool.query(
    `insert into friend (user1Id, user2Id) values ($1, $2)`,
    [user1Id, user2Id]
  )
}

export const confirmRequest = async (user1Id, user2Id) => {
  const res = await pool.query(
    `update friend set confirmed = true where user1Id = $1 and user2Id = $2`,
    [user1Id, user2Id]
  )
}

export const removeFriend = async (user1Id, user2Id) => {
  const res = await pool.query(
    `delete from friend where user1Id = $1 and user2Id = $2`,
    [user1Id, user2Id]
  )
}

export const readFriends = async (userId) => {
  const res = await pool.query(
    `select * from friend where user1Id = $1 or user2Id = $2`,
    [userId, userId]
  )
  return res.rows
}

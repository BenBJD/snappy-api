import pool from "./connection.js"

export const createSnap = async (fromUserId, toUserId) => {
  const res = await pool.query(
    `insert into snap ("fromUserId", "toUserId") values ($1, $2)`,
    [fromUserId, toUserId]
  )
}

export const readSnaps = async (id) => {
  const res = await pool.query(
    `select * from snap where "toUserId" = $1 or "fromUserId" = $2`,
    [id, id]
  )
  return res.rows
}

export const removeSnap = async (id) => {
  const res = await pool.query(`delete from snap where id = $1`, [id])
}

export const seenSnap = async (id) => {
  const res = await pool.query(`update snap set seen = true where id = $1`, [
    id,
  ])
}

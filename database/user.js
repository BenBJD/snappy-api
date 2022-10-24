import pool from "./connection.js"
import { hash, compare } from "bcrypt"
import { randomUUID } from "crypto"

// Create a new user
export const createUser = async (username, password) => {
  hash(password, 10, async (err, passwordHash) => {
    const res = await pool.query(
      `insert into "user" (username, "passwordHash") values ($1, $2)`,
      [username, passwordHash]
    )
  })
}

// Get a user's info
export const readUser = async (id) => {
  const res = await pool.query(
    `select (id, username, "snappyScore") from "user" where id = $1`,
    [id]
  )
  return res.rows[0]
}

// Check a password given a username and return the user's id and whether the password is valid
export const checkPassword = async (username, password) => {
  const res = await pool.query(
    `select (id, "passwordHash") from "user" where username = $1`,
    [username]
  )
  // returns an array of [userId (uuid), passwordTrue (bool)]
  return [res.rows[0]["id"], compare(password, res.rows[0]["passwordHash"])]
}

// Delete user
export const deleteUser = async (id) => {
  const res = await pool.query(`delete from "user" where id = $1`, [id])
}

// Updaters
export const updateUsername = async (id, username) => {
  const res = await pool.query(
    `update "user" set "username" = $1 where id = $2`,
    [username, id]
  )
}

export const updatePassword = async (id, password) => {
  hash(password, 10, async (err, passwordHash) => {
    const res = await pool.query(
      `update "user" set "passwordHash" = $1 where id = $2`,
      [passwordHash, id]
    )
  })
}

export const incrementSnappyScore = async (id) => {
  const res = await pool.query(
    `update "user" set "snappyScore" = "snappyScore" + 1 where id = $1`,
    [id]
  )
}

// Generate a UUID for a new login token
export const newLoginToken = async (id) => {
  const uuid = randomUUID()
  const res = await pool.query(
    `update "user" set "loginToken" = ($1) where id = $2`,
    [uuid, id]
  )
  return uuid
}

// Check a login token
export const checkLoginToken = async (id, token) => {
  const res = await pool.query(
    `select ("loginToken") from "user" where id = $1`,
    [id]
  )
  return res.rows[0]["loginToken"] === token
}

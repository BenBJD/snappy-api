import express from "express"
import { createUser, readUser } from "../database/user.js"

export const router = express.Router()
router.use(express.urlencoded())

router.get("/get", async (req, res) => {
  let data = await readUser(req.params["id"])
  res.json(data)
})

router.post("/update", (req, res) => {
  res.send("change the friends")
})

router.post("/create", (req, res) => {
  console.log(req.body["username"], req.body["password"])
})

router.post("/delete", (req, res) => {
  res.send("kill the friends")
})

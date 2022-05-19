import express from "express"

export const router = express.Router()

router.get("/get", (req, res) => {
    res.send("get the friends")
})

router.post("/update", (req, res) => {
    res.send("change the friends")
})

router.put("/create", (req, res) => {
    res.send("create the friends")
})

router.post("/delete", (req, res) => {
    res.send("kill the friends")
})

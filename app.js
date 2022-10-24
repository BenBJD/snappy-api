import express from "express"
import "dotenv/config"

import { router as friendsRouter } from "./routes/friends.js"
import { router as snapsRouter } from "./routes/snaps.js"
import { router as usersRouter } from "./routes/users.js"

const app = express()

app.use("/friends", friendsRouter)
app.use("/snaps", snapsRouter)
app.use("/users", usersRouter)

app.listen(5764, () => {
  console.log("Listening...")
})

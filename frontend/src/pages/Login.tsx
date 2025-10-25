
import { useState } from "react";
import axios from "axios";
import { TextField, Button, Card, Typography } from "@mui/material";

export default function Login() {
  const [username, setUsername] = useState("");
  const [token, setToken] = useState("");

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://localhost:8000/auth/login", { username, token });
      alert(res.data.success ? "Login success!" : "Invalid 2FA token");
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <Card sx={{ p: 4, width: 300, mx: "auto", mt: 10 }}>
      <Typography variant="h6">2FA Login</Typography>
      <TextField label="Username" value={username} onChange={e => setUsername(e.target.value)} fullWidth margin="normal" />
      <TextField label="2FA Token" value={token} onChange={e => setToken(e.target.value)} fullWidth margin="normal" />
      <Button variant="contained" fullWidth onClick={handleLogin}>Login</Button>
    </Card>
  );
}

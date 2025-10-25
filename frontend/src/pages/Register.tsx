
import { useState } from "react";
import axios from "axios";
import { TextField, Button, Card, Typography } from "@mui/material";

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [qrCode, setQrCode] = useState("");

  const handleRegister = async () => {
    try {
      const res = await axios.post("http://localhost:8000/auth/register", { username, password });
      setQrCode(res.data.qr);
    } catch (err) {
      alert("Registration failed");
    }
  };

  return (
    <Card sx={{ p: 4, width: 300, mx: "auto", mt: 10 }}>
      <Typography variant="h6">Register</Typography>
      <TextField label="Username" value={username} onChange={e => setUsername(e.target.value)} fullWidth margin="normal" />
      <TextField label="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} fullWidth margin="normal" />
      <Button variant="contained" fullWidth onClick={handleRegister}>Register</Button>
      {qrCode && <img src={`data:image/png;base64,${qrCode}`} alt="QR Code" />}
    </Card>
  );
}

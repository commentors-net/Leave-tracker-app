
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { TextField, Button, Card, Typography, Box } from "@mui/material";
import { authApi } from "@services/api";

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [qrCode, setQrCode] = useState("");
  const [secret, setSecret] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      const res = await authApi.register({ username, password });
      setQrCode(res.qr);
      setSecret(res.secret);
    } catch (err) {
      alert("Registration failed");
    }
  };

  const handleContinueToLogin = () => {
    navigate("/login");
  };

  return (
    <Card sx={{ p: 4, width: 400, mx: "auto", mt: 10 }}>
      <Typography variant="h6">Register</Typography>
      {!qrCode ? (
        <>
          <TextField label="Username" value={username} onChange={e => setUsername(e.target.value)} fullWidth margin="normal" />
          <TextField label="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} fullWidth margin="normal" />
          <Button variant="contained" fullWidth onClick={handleRegister}>Register</Button>
        </>
      ) : (
        <Box sx={{ textAlign: "center" }}>
          <Typography variant="body1" sx={{ mt: 2, mb: 2 }}>
            Scan this QR code with Google Authenticator or similar app:
          </Typography>
          <img src={`data:image/png;base64,${qrCode}`} alt="QR Code" style={{ maxWidth: "100%" }} />
          <Typography variant="body2" sx={{ mt: 2, mb: 2, wordBreak: "break-all" }}>
            Secret Key: <strong>{secret}</strong>
          </Typography>
          <Button variant="contained" fullWidth onClick={handleContinueToLogin} sx={{ mt: 2 }}>
            Continue to Login
          </Button>
        </Box>
      )}
    </Card>
  );
}

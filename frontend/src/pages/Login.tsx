
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { TextField, Button, Card, Typography } from "@mui/material";
import { authApi } from "@services/api";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await authApi.login({ username, password, token });
      
      // Store JWT token in localStorage
      localStorage.setItem("access_token", res.access_token);
      localStorage.setItem("username", res.username);
      
      // Trigger storage event for app state update
      window.dispatchEvent(new Event('storage'));
      
      alert("Login successful!");
      // Redirect to dashboard
      navigate("/dashboard");
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || "Login failed: Invalid credentials or 2FA token";
      alert(errorMsg);
    }
  };

  return (
    <Card sx={{ p: 4, width: 300, mx: "auto", mt: 10 }}>
      <Typography variant="h6">2FA Login</Typography>
      <TextField label="Username" value={username} onChange={e => setUsername(e.target.value)} fullWidth margin="normal" />
      <TextField 
        label="Password" 
        type="password"
        value={password} 
        onChange={e => setPassword(e.target.value)} 
        fullWidth 
        margin="normal" 
      />
      <TextField label="2FA Token" value={token} onChange={e => setToken(e.target.value)} fullWidth margin="normal" />
      <Button variant="contained" fullWidth onClick={handleLogin}>Login</Button>
    </Card>
  );
}

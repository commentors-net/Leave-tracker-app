import { useState, useEffect } from "react";
import axios from "axios";
import {
  Card,
  Typography,
  TextField,
  Button,
  Box,
  List,
  ListItem,
  ListItemText,
  Divider,
} from "@mui/material";

export default function Settings() {
  const [people, setPeople] = useState<any[]>([]);
  const [types, setTypes] = useState<any[]>([]);
  const [newPersonName, setNewPersonName] = useState("");
  const [newTypeName, setNewTypeName] = useState("");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const peopleRes = await axios.get("http://localhost:8000/api/people");
      setPeople(peopleRes.data);
      const typesRes = await axios.get("http://localhost:8000/api/types");
      setTypes(typesRes.data);
    } catch (err) {
      console.error("Failed to fetch data", err);
    }
  };

  const handleAddPerson = async () => {
    if (!newPersonName.trim()) return;
    try {
      await axios.post("http://localhost:8000/api/people", { name: newPersonName });
      setNewPersonName("");
      fetchData();
    } catch (err) {
      alert("Failed to add person");
    }
  };

  const handleAddType = async () => {
    if (!newTypeName.trim()) return;
    try {
      await axios.post("http://localhost:8000/api/types", { name: newTypeName });
      setNewTypeName("");
      fetchData();
    } catch (err) {
      alert("Failed to add type");
    }
  };

  return (
    <Box sx={{ display: "flex", gap: 4, mt: 4, flexWrap: "wrap" }}>
      <Card sx={{ p: 4, flex: 1, minWidth: 300 }}>
        <Typography variant="h6" gutterBottom>
          Manage People
        </Typography>
        <Box sx={{ display: "flex", gap: 2, mb: 2 }}>
          <TextField
            label="Person Name"
            value={newPersonName}
            onChange={(e) => setNewPersonName(e.target.value)}
            fullWidth
          />
          <Button variant="contained" onClick={handleAddPerson}>
            Add
          </Button>
        </Box>
        <Divider sx={{ my: 2 }} />
        <List>
          {people.map((person) => (
            <ListItem key={person.id}>
              <ListItemText primary={person.name} />
            </ListItem>
          ))}
        </List>
      </Card>

      <Card sx={{ p: 4, flex: 1, minWidth: 300 }}>
        <Typography variant="h6" gutterBottom>
          Manage Leave Types
        </Typography>
        <Box sx={{ display: "flex", gap: 2, mb: 2 }}>
          <TextField
            label="Type Name"
            value={newTypeName}
            onChange={(e) => setNewTypeName(e.target.value)}
            fullWidth
          />
          <Button variant="contained" onClick={handleAddType}>
            Add
          </Button>
        </Box>
        <Divider sx={{ my: 2 }} />
        <List>
          {types.map((type) => (
            <ListItem key={type.id}>
              <ListItemText primary={type.name} />
            </ListItem>
          ))}
        </List>
      </Card>
    </Box>
  );
}


import { useState, useEffect } from "react";
import axios from "axios";
import { TextField, Button, Card, Typography, Select, MenuItem, InputLabel, FormControl } from "@mui/material";

export default function Dashboard() {
  const [people, setPeople] = useState([]);
  const [types, setTypes] = useState([]);
  const [selectedPerson, setSelectedPerson] = useState("");
  const [selectedType, setSelectedType] = useState("");
  const [date, setDate] = useState("");
  const [duration, setDuration] = useState("");
  const [reason, setReason] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      const peopleRes = await axios.get("http://localhost:8000/api/people");
      setPeople(peopleRes.data);
      const typesRes = await axios.get("http://localhost:8000/api/types");
      setTypes(typesRes.data);
    };
    fetchData();
  }, []);

  const handleSubmit = async () => {
    try {
      await axios.post("http://localhost:8000/api/absences", {
        person_id: selectedPerson,
        type_id: selectedType,
        date,
        duration,
        reason,
      });
      alert("Absence logged successfully!");
    } catch (err) {
      alert("Failed to log absence");
    }
  };

  return (
    <Card sx={{ p: 4, width: 500, mx: "auto", mt: 10 }}>
      <Typography variant="h6">Log Absence</Typography>
      <FormControl fullWidth margin="normal">
        <InputLabel>Person</InputLabel>
        <Select value={selectedPerson} onChange={(e) => setSelectedPerson(e.target.value)}>
          {people.map((person: any) => (
            <MenuItem key={person.id} value={person.id}>{person.name}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <TextField type="date" value={date} onChange={(e) => setDate(e.target.value)} fullWidth margin="normal" />
      <FormControl fullWidth margin="normal">
        <InputLabel>Duration</InputLabel>
        <Select value={duration} onChange={(e) => setDuration(e.target.value)}>
          <MenuItem value="First Half">First Half</MenuItem>
          <MenuItem value="Second Half">Second Half</MenuItem>
          <MenuItem value="Full Day">Full Day</MenuItem>
        </Select>
      </FormControl>
      <FormControl fullWidth margin="normal">
        <InputLabel>Type</InputLabel>
        <Select value={selectedType} onChange={(e) => setSelectedType(e.target.value)}>
          {types.map((type: any) => (
            <MenuItem key={type.id} value={type.id}>{type.name}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <TextField label="Reason" value={reason} onChange={(e) => setReason(e.target.value)} fullWidth margin="normal" />
      <Button variant="contained" fullWidth onClick={handleSubmit}>Submit</Button>
    </Card>
  );
}

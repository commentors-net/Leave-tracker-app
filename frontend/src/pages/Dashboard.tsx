
import { useState, useEffect } from "react";
import { TextField, Button, Card, Typography, Select, MenuItem, InputLabel, FormControl } from "@mui/material";
import { peopleApi, typesApi, absencesApi } from "@services/api";
import type { Person, LeaveType } from "@services/api";

export default function Dashboard() {
  const [people, setPeople] = useState<Person[]>([]);
  const [types, setTypes] = useState<LeaveType[]>([]);
  const [selectedPerson, setSelectedPerson] = useState("");
  const [selectedType, setSelectedType] = useState("");
  const [date, setDate] = useState("");
  const [duration, setDuration] = useState("");
  const [reason, setReason] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [peopleData, typesData] = await Promise.all([
          peopleApi.getAll(),
          typesApi.getAll()
        ]);
        setPeople(peopleData);
        setTypes(typesData);
      } catch (err) {
        console.error("Failed to fetch data:", err);
        alert("Failed to load data. Please login again.");
      }
    };
    fetchData();
  }, []);

  const handleSubmit = async () => {
    try {
      await absencesApi.create({
        person_id: Number(selectedPerson),
        type_id: Number(selectedType),
        date,
        duration,
        reason,
      });
      alert("Absence logged successfully!");
      
      // Clear the form
      setSelectedPerson("");
      setSelectedType("");
      setDate("");
      setDuration("");
      setReason("");
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
          {people.map((person) => (
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
          {types.map((type) => (
            <MenuItem key={type.id} value={type.id}>{type.name}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <TextField label="Reason" value={reason} onChange={(e) => setReason(e.target.value)} fullWidth margin="normal" />
      <Button variant="contained" fullWidth onClick={handleSubmit}>Submit</Button>
    </Card>
  );
}

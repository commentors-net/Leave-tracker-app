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
  Tabs,
  Tab,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`settings-tabpanel-${index}`}
      aria-labelledby={`settings-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

export default function Settings() {
  const [people, setPeople] = useState<any[]>([]);
  const [types, setTypes] = useState<any[]>([]);
  const [newPersonName, setNewPersonName] = useState("");
  const [newTypeName, setNewTypeName] = useState("");
  const [tabValue, setTabValue] = useState(0);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editItem, setEditItem] = useState<any>(null);
  const [editName, setEditName] = useState("");
  const [editType, setEditType] = useState<"person" | "type">("person");

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

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleEditClick = (item: any, type: "person" | "type") => {
    setEditItem(item);
    setEditName(item.name);
    setEditType(type);
    setEditDialogOpen(true);
  };

  const handleEditSave = async () => {
    if (!editName.trim() || !editItem) return;
    try {
      const endpoint = editType === "person" ? "people" : "types";
      await axios.put(`http://localhost:8000/api/${endpoint}/${editItem.id}`, { name: editName });
      setEditDialogOpen(false);
      setEditItem(null);
      setEditName("");
      fetchData();
    } catch (err) {
      alert(`Failed to update ${editType}`);
    }
  };

  const handleDelete = async (id: number, type: "person" | "type") => {
    if (!confirm(`Are you sure you want to delete this ${type}?`)) return;
    try {
      const endpoint = type === "person" ? "people" : "types";
      await axios.delete(`http://localhost:8000/api/${endpoint}/${id}`);
      fetchData();
    } catch (err) {
      alert(`Failed to delete ${type}`);
    }
  };

  return (
    <Card sx={{ mt: 4, mx: "auto", maxWidth: 800 }}>
      <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="settings tabs">
          <Tab label="People" />
          <Tab label="Leave Types" />
        </Tabs>
      </Box>
      
      <TabPanel value={tabValue} index={0}>
        <Typography variant="h6" gutterBottom>
          Manage People
        </Typography>
        <Box sx={{ display: "flex", gap: 2, mb: 2 }}>
          <TextField
            label="Person Name"
            value={newPersonName}
            onChange={(e) => setNewPersonName(e.target.value)}
            fullWidth
            onKeyPress={(e) => e.key === "Enter" && handleAddPerson()}
          />
          <Button variant="contained" onClick={handleAddPerson}>
            Add
          </Button>
        </Box>
        <Divider sx={{ my: 2 }} />
        <Typography variant="subtitle2" color="text.secondary" gutterBottom>
          {people.length} {people.length === 1 ? "person" : "people"}
        </Typography>
        <List>
          {people.length === 0 ? (
            <ListItem>
              <ListItemText 
                primary="No people added yet" 
                secondary="Add people to track their leave"
              />
            </ListItem>
          ) : (
            people.map((person) => (
              <ListItem 
                key={person.id}
                secondaryAction={
                  <Box>
                    <IconButton edge="end" aria-label="edit" onClick={() => handleEditClick(person, "person")}>
                      <EditIcon />
                    </IconButton>
                    <IconButton edge="end" aria-label="delete" onClick={() => handleDelete(person.id, "person")}>
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                }
              >
                <ListItemText primary={person.name} />
              </ListItem>
            ))
          )}
        </List>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Typography variant="h6" gutterBottom>
          Manage Leave Types
        </Typography>
        <Box sx={{ display: "flex", gap: 2, mb: 2 }}>
          <TextField
            label="Leave Type Name"
            value={newTypeName}
            onChange={(e) => setNewTypeName(e.target.value)}
            fullWidth
            placeholder="e.g., Annual Leave, Sick Leave"
            onKeyPress={(e) => e.key === "Enter" && handleAddType()}
          />
          <Button variant="contained" onClick={handleAddType}>
            Add
          </Button>
        </Box>
        <Divider sx={{ my: 2 }} />
        <Typography variant="subtitle2" color="text.secondary" gutterBottom>
          {types.length} {types.length === 1 ? "type" : "types"}
        </Typography>
        <List>
          {types.length === 0 ? (
            <ListItem>
              <ListItemText 
                primary="No leave types added yet" 
                secondary="Add leave types like Annual Leave, Sick Leave, etc."
              />
            </ListItem>
          ) : (
            types.map((type) => (
              <ListItem 
                key={type.id}
                secondaryAction={
                  <Box>
                    <IconButton edge="end" aria-label="edit" onClick={() => handleEditClick(type, "type")}>
                      <EditIcon />
                    </IconButton>
                    <IconButton edge="end" aria-label="delete" onClick={() => handleDelete(type.id, "type")}>
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                }
              >
                <ListItemText primary={type.name} />
              </ListItem>
            ))
          )}
        </List>
      </TabPanel>

      {/* Edit Dialog */}
      <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)}>
        <DialogTitle>Edit {editType === "person" ? "Person" : "Leave Type"}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Name"
            type="text"
            fullWidth
            value={editName}
            onChange={(e) => setEditName(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleEditSave()}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleEditSave} variant="contained">Save</Button>
        </DialogActions>
      </Dialog>
    </Card>
  );
}

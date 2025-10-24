import React from 'react';
import { AppBar, Toolbar, Typography, Container } from '@mui/material';

function App() {
  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">
            Leave Tracker
          </Typography>
        </Toolbar>
      </AppBar>
      <Container>
        {/* The rest of your application will go here */}
      </Container>
    </div>
  );
}

export default App;

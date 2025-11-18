import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom';
import './index.css'
import App from './App.tsx'

import { UserProvider } from './context/UserContext';
import { SnackbarsProvider } from './context/SnackbarsContext.tsx';
import { GlobalModalDialogProvider } from './context/GlobalModalDialogContext.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>

      <SnackbarsProvider>
      <UserProvider>
      <GlobalModalDialogProvider>
        <App />
      </GlobalModalDialogProvider>
      </UserProvider>
      </SnackbarsProvider>

    </BrowserRouter>
  </StrictMode>,
)

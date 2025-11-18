import { Routes, Route } from 'react-router-dom';

import CreateAccount from './pages/CreateAccount';
import MyAccount from './pages/MyAccount';
import PriceHistory from './pages/PriceHistory';
import Tickers from './pages/Tickers';
import AdminDashboard from './pages/admin/Dashboard';
import Landing from './pages/Landing';
import GlobalNavBar from './components/GlobalNavBar';

export const API_ORIGIN = "https://specific-brande-data-group-585a3e34.koyeb.app";

import { Button } from "./components/ui/button"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "./components/ui/dialog"
import SignIn from './components/SignIn';

import { useContext } from 'react';
import { GlobalModalDialogContext } from './context/GlobalModalDialogContext';

function App() {
  const signInDialog = useContext(GlobalModalDialogContext);

  return (
    <>
    <div>
    <GlobalNavBar/>
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/register" element={<CreateAccount />} />
      <Route path="/me" element={<MyAccount />} />
      <Route path="/pricehistory/:tickerSymbol" element={<PriceHistory />} />
      <Route path="/tickers" element={<Tickers />} />
      <Route path="/admin" element={<AdminDashboard />} />
    </Routes>
    </div>

    {(()=>{if (signInDialog) {
      return (<Dialog>
        <DialogContent className="sm:max-w-md">
          <DialogHeader className="sm:justify-start">
            <DialogClose asChild>
              <Button type="button" variant="secondary">
                Close
              </Button>
            </DialogClose>
          </DialogHeader>

          <SignIn/>
        </DialogContent>
      </Dialog>);
    }
    return undefined;
    })()}
    </>
  );
}

export default App;
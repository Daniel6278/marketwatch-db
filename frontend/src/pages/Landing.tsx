import { Button } from "../components/ui/button";
import { Link } from 'react-router-dom';


function Landing() {
  return (
    <main>
        <h1>MarketWatch DB Project</h1>
        <div className="grid grid-cols-1">
            <Button asChild>
                <Link to="https://github.com/Daniel6278/marketwatch-db">GitHub Repo</Link>
            </Button>
            <Button asChild>
                <Link to="https://github.com/Daniel6278/marketwatch-db/tree/main/backend/api/sql">SQL Code</Link>
            </Button>
            <Button asChild>
                <Link to="https://github.com/Daniel6278/marketwatch-db/tree/main/backend/api/API_ENDPOINTS_DOCUMENTATION.md">API Documentation</Link>
            </Button>
        </div>
    </main>
  );
}

export default Landing;
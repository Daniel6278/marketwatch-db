import { Button } from "../components/ui/button";
import { Link } from 'react-router-dom';


function Landing() {
  return (
    <main>
        <h1 className="my-5">MarketWatch DB Project</h1>
        <div className="grid grid-cols-1 gap-2 md:grid-cols-3">
            <Button asChild className="!text-white">
                <a href="https://github.com/Daniel6278/marketwatch-db">GitHub Repo</a>
            </Button>
            <Button asChild className="!text-white">
                <a href="https://github.com/Daniel6278/marketwatch-db/tree/main/backend/api/sql">SQL Code</a>
            </Button>
            <Button asChild className="!text-white">
                <a href="https://github.com/Daniel6278/marketwatch-db/tree/main/backend/api/API_ENDPOINTS_DOCUMENTATION.md">API Documentation</a>
            </Button>
        </div>
    </main>
  );
}

export default Landing;
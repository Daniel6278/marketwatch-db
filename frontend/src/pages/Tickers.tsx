import { Link } from 'react-router-dom';
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "../components/ui/table";
import { Input } from "../components/ui/input";
import { useState, useEffect } from 'react';

import { API_ORIGIN } from '../App';

interface Ticker {
    tickerSymbol: string;
    company: string;
    lastPrice: number;
}

function Tickers() {

    const [currentTickers, setCurrentTickers] = useState<Ticker[]>([]);
    const [searchBarValue, setSearchBarValue] = useState<string>('');

    async function queryTickers() {
        const params = new URLSearchParams({
            'search_query': searchBarValue
        });
        const url = `${API_ORIGIN}/tickers${searchBarValue && searchBarValue.length ? ('?' + params.toString()) : ''}`;
        try {
            const response = await fetch(url);
            if (!response.ok) {
            throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setCurrentTickers(data); // updates state
            
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    useEffect(() => {
        queryTickers();
    }, []); // The empty dependency array ensures this effect runs only once on mount

    function onSearchBarChange(event: React.ChangeEvent<HTMLInputElement>) {
        setSearchBarValue((event.target as HTMLInputElement)?.value);

        queryTickers();
    }

  return (
    <main>
        <h1>Tickers</h1>
        <div>
            <Input onChange={onSearchBarChange} value={searchBarValue}></Input>
        </div>
        <Table>
        <TableHeader>
            <TableRow>
            <TableHead className="w-[100px]">Ticker Symbol</TableHead>
            <TableHead>Company Name</TableHead>
            <TableHead className="text-right">Last Price</TableHead>
            </TableRow>
        </TableHeader>
        <TableBody>
            {currentTickers.map((ticker) => (
            <TableRow key={ticker.tickerSymbol}>
                <TableCell className="font-medium">
                    <Link to={`/pricehistory/${ticker.tickerSymbol}`}>{ticker.tickerSymbol}</Link>
                </TableCell>
                <TableCell>{ticker.company}</TableCell>
                <TableCell className="text-right">{ticker.lastPrice}</TableCell>
            </TableRow>
            ))}
        </TableBody>
        </Table>
    </main>
  );
}

export default Tickers;
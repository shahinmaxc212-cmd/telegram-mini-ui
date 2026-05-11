// ── Live Crypto Prices (CoinGecko API) ──────────────────────────────────────
const COINS = ['bitcoin','ethereum','tether','binancecoin','solana','ripple'];
const COIN_MAP = {
    bitcoin:     { sym:'BTC',  icon:'₿',  name:'Bitcoin'   },
    ethereum:    { sym:'ETH',  icon:'Ξ',  name:'Ethereum'  },
    tether:      { sym:'USDT', icon:'₮',  name:'Tether'    },
    binancecoin: { sym:'BNB',  icon:'🔶', name:'BNB'       },
    solana:      { sym:'SOL',  icon:'◎',  name:'Solana'    },
    ripple:      { sym:'XRP',  icon:'✕',  name:'XRP'       },
};

let cryptoPrices = {};

const FALLBACK = {
    bitcoin:     { usd:103500, usd_24h_change: 2.4  },
    ethereum:    { usd:2580,   usd_24h_change: 1.8  },
    tether:      { usd:1.00,   usd_24h_change: 0.01 },
    binancecoin: { usd:710,    usd_24h_change: 3.1  },
    solana:      { usd:185,    usd_24h_change:-1.2  },
    ripple:      { usd:2.45,   usd_24h_change: 5.3  },
};

async function fetchCryptoPrices() {
    try {
        const ids = COINS.join(',');
        const r = await fetch(
            `https://api.coingecko.com/api/v3/simple/price?ids=${ids}&vs_currencies=usd&include_24hr_change=true`
        );
        if (!r.ok) throw new Error('API error');
        const data = await r.json();
        cryptoPrices = data;
        updateAllPriceDisplays(data);
    } catch {
        cryptoPrices = FALLBACK;
        updateAllPriceDisplays(FALLBACK);
    }
}

function formatPrice(p) {
    if (p >= 1000) return '$' + p.toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2});
    if (p >= 1)    return '$' + p.toFixed(4);
    return '$' + p.toFixed(6);
}

function updateAllPriceDisplays(data) {
    // Ticker
    let tickerContent = '';
    COINS.forEach(id => {
        if (!data[id]) return;
        const meta = COIN_MAP[id];
        const price = data[id].usd;
        const chg   = data[id].usd_24h_change || 0;
        const sign  = chg >= 0 ? '+' : '';
        const cls   = chg >= 0 ? 'ticker-change-pos' : 'ticker-change-neg';
        tickerContent += `<span class="ticker-item">
            <span class="ticker-symbol">${meta.sym}</span>
            <span class="ticker-price">${formatPrice(price)}</span>
            <span class="${cls}">${sign}${chg.toFixed(2)}%</span>
        </span>`;
    });
    document.querySelectorAll('.ticker-inner').forEach(el => {
        el.innerHTML = tickerContent + tickerContent;  // duplicate for seamless loop
    });

    // Market cards & inline price displays
    COINS.forEach(id => {
        if (!data[id]) return;
        const price = data[id].usd;
        const chg   = data[id].usd_24h_change || 0;
        const sign  = chg >= 0 ? '+' : '';
        const cls   = chg >= 0 ? 'pos' : 'neg';

        document.querySelectorAll(`[data-coin="${id}"] .market-coin-price`).forEach(el => {
            el.textContent = formatPrice(price);
        });
        document.querySelectorAll(`[data-coin="${id}"] .market-coin-change`).forEach(el => {
            el.textContent = `${sign}${chg.toFixed(2)}%`;
            el.className = `market-coin-change ${cls}`;
        });
        document.querySelectorAll(`[data-coin-price="${id}"]`).forEach(el => {
            el.textContent = formatPrice(price);
        });
        document.querySelectorAll(`[data-coin-chg="${id}"]`).forEach(el => {
            el.textContent = `${sign}${chg.toFixed(2)}%`;
            el.className = `price-chg ${cls}`;
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    fetchCryptoPrices();
    setInterval(fetchCryptoPrices, 30_000);
});

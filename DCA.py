npm install axios
const axios = require('axios');

// Function to fetch historical price data
const fetchHistoricalData = async (symbol, apiKey) => {
  const url = `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=${symbol}&outputsize=full&apikey=${apiKey}`;

  try {
    const response = await axios.get(url);
    const data = response.data['Time Series (Daily)'];
    if (!data) {
      throw new Error('Invalid data format or API limit exceeded');
    }
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
    return null;
  }
};

const apiKey = 'YOUR_ALPHA_VANTAGE_API_KEY';
fetchHistoricalData('SPY', apiKey).then(data => {
  console.log(data);
});

// Function to process historical price data
const processHistoricalData = (data) => {
  return Object.keys(data).map(date => ({
    date,
    close: parseFloat(data[date]['4. close']),
  })).sort((a, b) => new Date(a.date) - new Date(b.date));
};

// Example usage
fetchHistoricalData('SPY', apiKey).then(data => {
  if (data) {
    const processedData = processHistoricalData(data);
    console.log(processedData);
  }
});



// Function to simulate dollar-cost averaging
const simulateDCA = (historicalData, startDate, endDate, principal, investAmount, interval) => {
  let balance = principal;
  let totalShares = 0;
  let totalInvested = principal;

  // Filter data for the specified date range
  const filteredData = historicalData.filter(entry => new Date(entry.date) >= new Date(startDate) && new Date(entry.date) <= new Date(endDate));

  // Determine the interval in days
  const intervalInDays = interval === 'weekly' ? 7 : (interval === 'bi-weekly' ? 14 : 30);

  // Loop through the filtered data at the specified intervals
  for (let i = 0; i < filteredData.length; i += intervalInDays) {
    const price = filteredData[i].close;
    const sharesBought = investAmount / price;
    totalShares += sharesBought;
    balance -= investAmount;
    totalInvested += investAmount;
  }

  // Calculate the value of the investment at the end date
  const finalPrice = filteredData[filteredData.length - 1].close;
  const finalValue = totalShares * finalPrice;

  return {
    totalInvested,
    finalValue,
    totalShares,
    balance
  };
};

// Example usage
fetchHistoricalData('SPY', apiKey).then(data => {
  if (data) {
    const processedData = processHistoricalData(data);
    const result = simulateDCA(processedData, '2020-01-01', '2022-01-01', 1000, 100, 'monthly');
    console.log(result);
  }
});

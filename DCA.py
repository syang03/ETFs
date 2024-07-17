// Function to simulate dollar-cost averaging
const simulateDCA = (historicalData, startDate, endDate, principal, investAmount, interval) => {
  let balance = principal;
  let totalShares = 0;
  let totalInvested = principal;

  // Filter data for the specified date range
  const filteredData = historicalData.filter(entry => new Date(entry.date) >= new Date(startDate) && new Date(entry.date) <= new Date(endDate));

  // Determine the interval by days
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

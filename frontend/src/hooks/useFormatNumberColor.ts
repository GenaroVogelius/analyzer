export const FormatNumberColor = (
  value: number | string,
  sign?: { isBeforeValue: boolean, sign: string },
  decimals: number = 2,
  thousandSeparator?: boolean
) => {
  const formattedValue =
    typeof value === "number"
      ? thousandSeparator
        ? value
            .toLocaleString("en-US", {
              minimumFractionDigits: decimals,
              maximumFractionDigits: decimals,
            })
            .replace(/,/g, ".")
        : value.toFixed(decimals)
      : value;
  const isPositive = typeof value === "number" && value >= 0;
  const displayValue = sign ? `${sign.isBeforeValue ? sign.sign : ""}${formattedValue}${sign.isBeforeValue ? "" : sign.sign}` : formattedValue;
  const className = `font-medium ${
    isPositive ? "text-green-600" : "text-red-600"
  }`;

  return { displayValue, className };
};

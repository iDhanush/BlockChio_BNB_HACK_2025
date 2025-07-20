import "./globals.css";

export const metadata = {
  title: "Blockchio",
  description: "Blockchio | Decentralized AI Playground",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head />
      <body>{children}</body>
    </html>
  );
}

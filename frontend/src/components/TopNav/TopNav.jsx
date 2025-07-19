"use client";

import "./TopNav.scss";
import Link from "next/link";
import { useState, useEffect, useMemo, memo } from "react";
import { useAccount } from "wagmi";
import "@rainbow-me/rainbowkit/styles.css";
import {
  getDefaultConfig,
  RainbowKitProvider,
  darkTheme,
  ConnectButton,
} from "@rainbow-me/rainbowkit";
import { WagmiProvider } from "wagmi";
import { mainnet, polygon, optimism, arbitrum, base } from "wagmi/chains";
import { QueryClientProvider, QueryClient } from "@tanstack/react-query";
import { usePathname } from "next/navigation";

// Create singletons outside component to prevent recreation on every render
const config = getDefaultConfig({
  appName: "Dgent",
  projectId: "YOUR_PROJECT_ID", // Get this from https://cloud.walletconnect.com
  chains: [mainnet, polygon, optimism, arbitrum, base],
  ssr: true,
});

const queryClient = new QueryClient();

// Pre-configured theme to avoid recreation
const rainbowKitTheme = darkTheme({
  accentColor: "",
  accentColorForeground: "#FF7D2B",
  borderRadius: "small",
  fontStack: "system",
  overlayBlur: "small",
});

// Memoized WalletLogger component to prevent unnecessary re-renders
const WalletLogger = memo(() => {
  const { address, isConnected } = useAccount();

  useEffect(() => {
    if (isConnected && address) {
      console.log("Wallet connected - Address:", address);
    } else {
      console.log("Wallet disconnected");
    }
  }, [isConnected, address]);

  return <ConnectButton label="Sign In" accountStatus="avatar" />;
});

// Memoized NavContent to prevent re-renders when providers don't change
const NavContent = memo(() => {
  const pathname = usePathname();

  // Memoize the background style to prevent unnecessary re-renders
  const backgroundStyle = useMemo(
    () => ({
      background: pathname === "/" ? "transperent" : "#101013",
      border: pathname === "/" ? "none" : "",
    }),
    [pathname]
  );

  return (
    <div className="top-nav" style={backgroundStyle}>
      <Link href="/" className="top-nav-left">
        BlockChio
      </Link>
      <div className="top-nav-center">hi</div>
      <div className="top-nav-right">
        <WalletLogger />
      </div>
    </div>
  );
});

const TopNav = () => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Don't render wallet functionality until mounted to prevent hydration issues
  if (!mounted) {
    return (
      <div className="top-nav" style={{ background: "#101013" }}>
        <Link href="/" className="top-nav-left">
          BlockChio
        </Link>
        <div className="top-nav-center">hi</div>
        <div className="top-nav-right">
          <div style={{ width: "120px", height: "40px" }}>
            {/* Placeholder for connect button */}
          </div>
        </div>
      </div>
    );
  }

  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider theme={rainbowKitTheme}>
          <NavContent />
        </RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
};

export default TopNav;

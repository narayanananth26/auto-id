import "./globals.css";

export const metadata = {
	title: "AUTO-ID: Real-time Number Plate Recognition",
	description:
		"A Real-time number plate recognition system using OpenALCR and Next.js",
};

export default function RootLayout({ children }) {
	return (
		<html lang="en">
			<body>{children}</body>
		</html>
	);
}

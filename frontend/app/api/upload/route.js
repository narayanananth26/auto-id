import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function POST(req) {
	const formData = await req.formData();
	const file = formData.get("file");

	if (!file) {
		return new NextResponse("No file uploaded", { status: 400 });
	}

	const uploadDir = path.join(process.cwd(), "public/uploads");
	const filePath = path.join(uploadDir, file.name);

	// Ensure the upload directory exists
	if (!fs.existsSync(uploadDir)) {
		fs.mkdirSync(uploadDir, { recursive: true });
	}

	// Save the file locally
	const buffer = await file.arrayBuffer();
	fs.writeFileSync(filePath, Buffer.from(buffer));

	return NextResponse.json({
		message: "File uploaded successfully",
		filePath,
	});
}

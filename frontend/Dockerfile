FROM node:latest

WORKDIR /app

COPY package*.json ./

RUN npm install --only=production
#RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

# Start the Next.js app using the production build
CMD ["npm", "run", "start"]
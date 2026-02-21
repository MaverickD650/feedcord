FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

COPY FeedCord.csproj ./
RUN dotnet restore

COPY src ./src
COPY restart-first-run.sh ./
RUN dotnet publish FeedCord.csproj -c Release -o /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/runtime:10.0 AS final
WORKDIR /app

COPY --from=build /app/publish ./
COPY --from=build /src/restart-first-run.sh ./
RUN chmod +x /app/restart-first-run.sh && chown -R 10001:10001 /app

USER 10001
ENTRYPOINT ["/app/restart-first-run.sh"]

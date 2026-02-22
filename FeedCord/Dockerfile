FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

COPY FeedCord.csproj ./
RUN dotnet restore

COPY src ./src
RUN dotnet publish FeedCord.csproj -c Release -o /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final
WORKDIR /app

COPY --chown=10001:10001 --from=build /app/publish ./

USER 10001
ENTRYPOINT ["dotnet", "FeedCord.dll"]

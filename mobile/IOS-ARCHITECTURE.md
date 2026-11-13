# iOS App Architecture - SwiftUI Implementation

## Tech Stack

```
Framework: SwiftUI (iOS 15.0+)
Architecture: MVVM + Clean Architecture
Language: Swift 5.9+
Package Manager: CocoaPods / SPM
Networking: URLSession + Combine
Database: Core Data + SwiftData
Local Storage: Keychain + UserDefaults
Maps: MapKit (native)
Authentication: AuthenticationServices + Custom
JSON: Codable + custom decoders
Testing: XCTest + SwiftUI Testing
Analytics: Firebase Analytics
Crash Reporting: Firebase Crashlytics
Push Notifications: APNs with Firebase Cloud Messaging
```

## Project Structure

```
ios/
├── YatraDiscover.xcodeproj
│   ├── YatraDiscover.xcconfig
│   └── Configurations/
│       ├── Debug.xcconfig
│       ├── Release.xcconfig
│       └── Dev.xcconfig
│
├── YatraDiscover/
│   ├── App/
│   │   ├── YatraDiscoverApp.swift (Main entry point)
│   │   └── Modifiers/
│   │       ├── NavigationModifier.swift
│   │       └── EnvironmentModifiers.swift
│   │
│   ├── Presentation/
│   │   ├── Screens/
│   │   │   ├── Splash/
│   │   │   │   ├── SplashView.swift
│   │   │   │   └── SplashViewModel.swift
│   │   │   │
│   │   │   ├── Authentication/
│   │   │   │   ├── LoginView.swift
│   │   │   │   ├── LoginViewModel.swift
│   │   │   │   ├── SignupView.swift
│   │   │   │   ├── SignupViewModel.swift
│   │   │   │   ├── ForgotPasswordView.swift
│   │   │   │   ├── ResetPasswordView.swift
│   │   │   │   └── EmailVerificationView.swift
│   │   │   │
│   │   │   ├── TabBar/
│   │   │   │   └── MainTabView.swift
│   │   │   │
│   │   │   ├── Dashboard/
│   │   │   │   ├── DashboardView.swift
│   │   │   │   ├── DashboardViewModel.swift
│   │   │   │   ├── UpcomingTripsView.swift
│   │   │   │   ├── RecentItinerariesView.swift
│   │   │   │   └── QuickStatsView.swift
│   │   │   │
│   │   │   ├── Itinerary/
│   │   │   │   ├── ItineraryListView.swift
│   │   │   │   ├── ItineraryListViewModel.swift
│   │   │   │   ├── ItineraryDetailView.swift
│   │   │   │   ├── ItineraryDetailViewModel.swift
│   │   │   │   ├── CreateItineraryView.swift
│   │   │   │   ├── CreateItineraryViewModel.swift
│   │   │   │   ├── DayDetailView.swift
│   │   │   │   ├── ActivityDetailView.swift
│   │   │   │   ├── EditActivityView.swift
│   │   │   │   ├── MapView.swift
│   │   │   │   └── ShareItineraryView.swift
│   │   │   │
│   │   │   ├── Bookings/
│   │   │   │   ├── BookingsListView.swift
│   │   │   │   ├── BookingsListViewModel.swift
│   │   │   │   ├── BookingDetailView.swift
│   │   │   │   ├── CheckoutView.swift
│   │   │   │   ├── PaymentView.swift
│   │   │   │   └── ConfirmationView.swift
│   │   │   │
│   │   │   ├── Saved/
│   │   │   │   ├── SavedDestinationsView.swift
│   │   │   │   ├── SavedDestinationsViewModel.swift
│   │   │   │   ├── DestinationDetailView.swift
│   │   │   │   └── WishlistView.swift
│   │   │   │
│   │   │   ├── Explore/
│   │   │   │   ├── ExploreView.swift
│   │   │   │   ├── ExploreViewModel.swift
│   │   │   │   ├── DestinationGridView.swift
│   │   │   │   ├── SearchView.swift
│   │   │   │   ├── FilterView.swift
│   │   │   │   └── CategoryView.swift
│   │   │   │
│   │   │   ├── AI/
│   │   │   │   ├── AIChatView.swift
│   │   │   │   ├── AIChatViewModel.swift
│   │   │   │   ├── ChatMessageView.swift
│   │   │   │   ├── SuggestionCardView.swift
│   │   │   │   └── LoadingAnimationView.swift
│   │   │   │
│   │   │   └── Settings/
│   │   │       ├── SettingsView.swift
│   │   │       ├── ProfileSettingsView.swift
│   │   │       ├── AccountSettingsView.swift
│   │   │       ├── NotificationPreferencesView.swift
│   │   │       ├── PrivacySettingsView.swift
│   │   │       ├── AboutView.swift
│   │   │       └── DarkModeToggleView.swift
│   │   │
│   │   ├── Components/
│   │   │   ├── Common/
│   │   │   │   ├── HeaderView.swift
│   │   │   │   ├── TabBarView.swift
│   │   │   │   ├── LoadingView.swift
│   │   │   │   ├── ErrorView.swift
│   │   │   │   ├── EmptyStateView.swift
│   │   │   │   ├── NavigationBar.swift
│   │   │   │   └── SafeAreaInsets.swift
│   │   │   │
│   │   │   ├── UI/
│   │   │   │   ├── CustomButton.swift
│   │   │   │   ├── CustomTextField.swift
│   │   │   │   ├── CustomSecureField.swift
│   │   │   │   ├── CustomPicker.swift
│   │   │   │   ├── CustomCard.swift
│   │   │   │   ├── CustomBadge.swift
│   │   │   │   ├── RatingView.swift
│   │   │   │   ├── PriceTag.swift
│   │   │   │   └── LocationTag.swift
│   │   │   │
│   │   │   ├── Modifiers/
│   │   │   │   ├── CardModifier.swift
│   │   │   │   ├── ButtonModifier.swift
│   │   │   │   ├── ShadowModifier.swift
│   │   │   │   ├── CornerRadiusModifier.swift
│   │   │   │   └── LoadingModifier.swift
│   │   │   │
│   │   │   └── Navigation/
│   │   │       ├── NavigationRouter.swift
│   │   │       ├── RouteModifier.swift
│   │   │       └── DeepLinkHandler.swift
│   │   │
│   │   └── Resources/
│   │       ├── Strings/
│   │       │   ├── Localizable.strings
│   │       │   ├── Localizable.strings (es)
│   │       │   ├── Localizable.strings (fr)
│   │       │   └── Localizable.strings (de)
│   │       │
│   │       ├── Colors/
│   │       │   └── ColorTheme.swift
│   │       │
│   │       ├── Fonts/
│   │       │   └── FontTheme.swift
│   │       │
│   │       ├── Images/
│   │       │   ├── Icons
│   │       │   ├── Illustrations
│   │       │   └── Logos
│   │       │
│   │       └── JSON/
│   │           └── mock-data.json
│   │
│   ├── Domain/
│   │   ├── Models/
│   │   │   ├── User.swift
│   │   │   ├── Itinerary.swift
│   │   │   ├── Activity.swift
│   │   │   ├── Destination.swift
│   │   │   ├── Booking.swift
│   │   │   ├── Review.swift
│   │   │   └── APIResponse.swift
│   │   │
│   │   ├── Repositories/
│   │   │   ├── AuthRepository.swift
│   │   │   ├── ItineraryRepository.swift
│   │   │   ├── BookingRepository.swift
│   │   │   ├── UserRepository.swift
│   │   │   └── AIRepository.swift
│   │   │
│   │   └── UseCases/
│   │       ├── AuthUseCases.swift
│   │       ├── ItineraryUseCases.swift
│   │       ├── BookingUseCases.swift
│   │       └── AIUseCases.swift
│   │
│   ├── Data/
│   │   ├── Network/
│   │   │   ├── APIClient.swift
│   │   │   ├── APIEnvironment.swift
│   │   │   ├── URLSession+Extensions.swift
│   │   │   ├── APILogger.swift
│   │   │   └── APIModels/
│   │   │       ├── AuthAPI.swift
│   │   │       ├── ItineraryAPI.swift
│   │   │       ├── BookingAPI.swift
│   │   │       └── AIAPI.swift
│   │   │
│   │   ├── LocalStorage/
│   │   │   ├── KeychainManager.swift
│   │   │   ├── UserDefaultsManager.swift
│   │   │   ├── CoreDataManager.swift
│   │   │   └── CacheManager.swift
│   │   │
│   │   └── Repositories/
│   │       ├── AuthRepositoryImpl.swift
│   │       ├── ItineraryRepositoryImpl.swift
│   │       ├── BookingRepositoryImpl.swift
│   │       └── UserRepositoryImpl.swift
│   │
│   ├── Utilities/
│   │   ├── Extensions/
│   │   │   ├── String+Extension.swift
│   │   │   ├── Date+Extension.swift
│   │   │   ├── View+Extension.swift
│   │   │   ├── Color+Extension.swift
│   │   │   ├── Double+Extension.swift
│   │   │   └── Error+Extension.swift
│   │   │
│   │   ├── Helpers/
│   │   │   ├── DateFormatter+Helper.swift
│   │   │   ├── NumberFormatter+Helper.swift
│   │   │   ├── CurrencyFormatter.swift
│   │   │   └── ValidationHelper.swift
│   │   │
│   │   ├── Constants/
│   │   │   ├── APIConstants.swift
│   │   │   ├── AppConstants.swift
│   │   │   ├── UIConstants.swift
│   │   │   └── EnvironmentVariables.swift
│   │   │
│   │   ├── Observers/
│   │   │   ├── AppLifecycleObserver.swift
│   │   │   ├── ReachabilityObserver.swift
│   │   │   └── LocationObserver.swift
│   │   │
│   │   └── Services/
│   │       ├── LocationService.swift
│   │       ├── NotificationService.swift
│   │       ├── AnalyticsService.swift
│   │       └── DeepLinkService.swift
│   │
│   ├── State/
│   │   ├── AuthStateManager.swift
│   │   ├── AppEnvironment.swift
│   │   └── AppDependencyContainer.swift
│   │
│   └── Resources/
│       ├── Assets.xcassets/
│       ├── Localizable.xcstrings
│       └── LaunchScreen.storyboard
│
├── YatraDiscoverTests/
│   ├── AuthViewModelTests.swift
│   ├── ItineraryViewModelTests.swift
│   ├── APIClientTests.swift
│   ├── RepositoryTests.swift
│   └── Mock/
│       ├── MockAPIClient.swift
│       ├── MockAuthRepository.swift
│       └── MockItineraryRepository.swift
│
├── YatraDiscoverUITests/
│   ├── AuthenticationUITests.swift
│   ├── ItineraryCreationUITests.swift
│   └── BookingFlowUITests.swift
│
├── Podfile
├── Podfile.lock
├── .gitignore
├── .swiftformat
├── .swiftlint.yml
├── Info.plist
└── README.md
```

## View Hierarchy

### Tab Navigation (5 Tabs)

```
MainTabView
├── Tab 1: Dashboard (Home icon)
│   └── DashboardView
│       ├── Quick Stats
│       ├── Upcoming Trips
│       └── Recent Itineraries
│
├── Tab 2: Explore (Compass icon)
│   └── ExploreView
│       ├── Search Bar
│       ├── Categories
│       ├── Destination Grid
│       └── Filters
│
├── Tab 3: Itineraries (List icon)
│   └── ItineraryListView
│       ├── My Itineraries
│       ├── Create Button
│       ├── Search/Filter
│       └── List of Itineraries
│
├── Tab 4: AI Chat (Message icon)
│   └── AIChatView
│       ├── Chat Messages
│       ├── Input Box
│       └── Suggestions
│
└── Tab 5: Profile (Person icon)
    └── ProfileView
        ├── User Info
        ├── Settings
        ├── Bookings
        └── Logout
```

## MVVM Pattern Implementation

### ViewModel Example

```swift
@MainActor
class ItineraryListViewModel: ObservableObject {
    @Published var itineraries: [Itinerary] = []
    @Published var isLoading = false
    @Published var error: AppError?
    
    private let repository: ItineraryRepository
    private var cancellables = Set<AnyCancellable>()
    
    init(repository: ItineraryRepository) {
        self.repository = repository
    }
    
    func loadItineraries() {
        isLoading = true
        repository.getItineraries()
            .receive(on: DispatchQueue.main)
            .sink { [weak self] completion in
                self?.isLoading = false
                if case .failure(let error) = completion {
                    self?.error = error
                }
            } receiveValue: { [weak self] itineraries in
                self?.itineraries = itineraries
            }
            .store(in: &cancellables)
    }
}
```

## Key Features

### 1. Authentication
- Biometric authentication (Face ID, Touch ID)
- OAuth integration (Apple Sign In, Google)
- Token refresh mechanism
- Secure token storage in Keychain

### 2. Itinerary Management
- Create itinerary with AI assistance
- Drag-and-drop activity reordering
- Edit/delete activities
- Day-by-day planning
- Share itinerary via link

### 3. AI Chat
- Real-time message streaming
- Context-aware responses
- Message history
- Suggestion cards

### 4. Maps Integration
- MapKit for native maps
- Activity location pinning
- Route visualization
- Distance calculation

### 5. Push Notifications
- Trip reminders
- Booking confirmations
- AI recommendations
- User engagement notifications

### 6. Offline Support
- Core Data caching
- Sync when connection restored
- Offline-first data model

## SwiftUI Best Practices

### State Management

```swift
// Use @StateObject for ViewModel ownership
// Use @ObservedObject for passed ViewModels
// Use @State for local UI state
// Use @Environment for app-wide state

@main
struct YatraDiscoverApp: App {
    @StateObject var authManager = AuthStateManager()
    
    var body: some Scene {
        WindowGroup {
            if authManager.isLoggedIn {
                MainTabView()
                    .environmentObject(authManager)
            } else {
                LoginView(authManager: authManager)
            }
        }
    }
}
```

### Performance Optimization

```swift
// Use LazyVStack for large lists
LazyVStack {
    ForEach(viewModel.itineraries) { itinerary in
        ItineraryRowView(itinerary: itinerary)
    }
}

// Use .id() for ForEach when order changes
ForEach(viewModel.activities, id: \.id) { activity in
    ActivityView(activity: activity)
}

// Use .equatable() modifier to prevent re-renders
Text(viewModel.title)
    .equatable()
```

## Networking

### API Client with Combine

```swift
protocol APIClientProtocol {
    func request<T: Decodable>(_ endpoint: APIEndpoint) -> AnyPublisher<T, AppError>
}

class APIClient: APIClientProtocol {
    private let session: URLSession
    private let baseURL: URL
    
    func request<T: Decodable>(_ endpoint: APIEndpoint) -> AnyPublisher<T, AppError> {
        guard let url = URL(string: endpoint.path, relativeTo: baseURL) else {
            return Fail(error: .invalidURL)
                .eraseToAnyPublisher()
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = endpoint.method.rawValue
        request.addAuthHeader()
        
        return session.dataTaskPublisher(for: request)
            .mapError { _ in AppError.networkError }
            .flatMap { data, response in
                guard let httpResponse = response as? HTTPURLResponse else {
                    return Fail(error: AppError.invalidResponse).eraseToAnyPublisher()
                }
                
                guard (200...299).contains(httpResponse.statusCode) else {
                    return Fail(error: AppError.httpError(httpResponse.statusCode)).eraseToAnyPublisher()
                }
                
                return Just(data).setFailureType(to: AppError.self).eraseToAnyPublisher()
            }
            .decode(type: T.self, decoder: JSONDecoder())
            .mapError { _ in AppError.decodingError }
            .eraseToAnyPublisher()
    }
}
```

## Testing Strategy

### Unit Tests

```swift
class ItineraryViewModelTests: XCTestCase {
    var viewModel: ItineraryListViewModel!
    var mockRepository: MockItineraryRepository!
    
    override func setUp() {
        super.setUp()
        mockRepository = MockItineraryRepository()
        viewModel = ItineraryListViewModel(repository: mockRepository)
    }
    
    func testLoadItineraries() {
        // Arrange
        let expectedItineraries = [Itinerary.mock(), Itinerary.mock()]
        mockRepository.getItinerariesResult = .success(expectedItineraries)
        
        // Act
        viewModel.loadItineraries()
        
        // Assert
        XCTAssertEqual(viewModel.itineraries, expectedItineraries)
    }
}
```

---

**Last Updated:** 2026-11-13
**Status:** Ready for development

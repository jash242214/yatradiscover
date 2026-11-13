# Android App Architecture - Jetpack Compose Implementation

## Tech Stack

```
Framework: Jetpack Compose (declarative UI)
Language: Kotlin 1.9+
Architecture: MVVM + Clean Architecture
Build System: Gradle KTS
Dependency Injection: Hilt
Networking: Retrofit + OkHttp
Serialization: Kotlinx Serialization
Database: Room + DataStore
Local Storage: EncryptedSharedPreferences
Maps: Google Maps API + Compose Maps
Authentication: Firebase Auth + Custom
Reactive: Coroutines + Flow
Testing: JUnit4 + Mockito + Espresso
Analytics: Firebase Analytics
Crash Reporting: Firebase Crashlytics
Push Notifications: Firebase Cloud Messaging
Image Loading: Coil / Glide
Navigation: Jetpack Navigation Compose
```

## Project Structure

```
android/
├── app/
│   ├── build.gradle.kts
│   ├── src/
│   │   ├── main/
│   │   │   ├── AndroidManifest.xml
│   │   │   ├── java/com/yatradiscover/
│   │   │   │   ├── YatraDiscoverApp.kt (Application class)
│   │   │   │   ├── MainActivity.kt
│   │   │   │   │
│   │   │   │   ├── di/
│   │   │   │   │   ├── AppModule.kt
│   │   │   │   │   ├── NetworkModule.kt
│   │   │   │   │   ├── DatabaseModule.kt
│   │   │   │   │   ├── RepositoryModule.kt
│   │   │   │   │   └── UseCaseModule.kt
│   │   │   │   │
│   │   │   │   ├── presentation/
│   │   │   │   │   ├── theme/
│   │   │   │   │   │   ├── Theme.kt
│   │   │   │   │   │   ├── Color.kt
│   │   │   │   │   │   ├── Typography.kt
│   │   │   │   │   │   └── Dimen.kt
│   │   │   │   │   │
│   │   │   │   │   ├── navigation/
│   │   │   │   │   │   ├── Navigation.kt
│   │   │   │   │   │   ├── NavigationDestination.kt
│   │   │   │   │   │   ├── NavGraphBuilder.kt
│   │   │   │   │   │   └── DeepLinkHandler.kt
│   │   │   │   │   │
│   │   │   │   │   ├── screens/
│   │   │   │   │   │   ├── splash/
│   │   │   │   │   │   │   ├── SplashScreen.kt
│   │   │   │   │   │   │   └── SplashViewModel.kt
│   │   │   │   │   │   │
│   │   │   │   │   │   ├── auth/
│   │   │   │   │   │   │   ├── login/
│   │   │   │   │   │   │   │   ├── LoginScreen.kt
│   │   │   │   │   │   │   │   └── LoginViewModel.kt
│   │   │   │   │   │   │   ├── signup/
│   │   │   │   │   │   │   │   ├── SignupScreen.kt
│   │   │   │   │   │   │   │   └── SignupViewModel.kt
│   │   │   │   │   │   │   ├── forgot_password/
│   │   │   │   │   │   │   │   ├── ForgotPasswordScreen.kt
│   │   │   │   │   │   │   │   └── ForgotPasswordViewModel.kt
│   │   │   │   │   │   │   └── email_verification/
│   │   │   │   │   │   │       └── EmailVerificationScreen.kt
│   │   │   │   │   │   │
│   │   │   │   │   │   ├── dashboard/
│   │   │   │   │   │   │   ├── DashboardScreen.kt
│   │   │   │   │   │   │   ├── DashboardViewModel.kt
│   │   │   │   │   │   │   ├── StatsCard.kt
│   │   │   │   │   │   │   ├── UpcomingTripsCard.kt
│   │   │   │   │   │   │   └── QuickActionCards.kt
│   │   │   │   │   │   │
│   │   │   │   │   │   ├── itinerary/
│   │   │   │   │   │   │   ├── list/
│   │   │   │   │   │   │   │   ├── ItineraryListScreen.kt
│   │   │   │   │   │   │   │   └── ItineraryListViewModel.kt
│   │   │   │   │   │   │   ├── detail/
│   │   │   │   │   │   │   │   ├── ItineraryDetailScreen.kt
│   │   │   │   │   │   │   │   ├── ItineraryDetailViewModel.kt
│   │   │   │   │   │   │   │   └── DayDetailScreen.kt
│   │   │   │   │   │   │   ├── create/
│   │   │   │   │   │   │   │   ├── CreateItineraryScreen.kt
│   │   │   │   │   │   │   │   ├── CreateItineraryViewModel.kt
│   │   │   │   │   │   │   │   ├── ActivityFormScreen.kt
│   │   │   │   │   │   │   │   └── DatePickerComposable.kt
│   │   │   │   │   │   │   ├── edit/
│   │   │   │   │   │   │   │   ├── EditItineraryScreen.kt
│   │   │   │   │   │   │   │   ├── EditItineraryViewModel.kt
│   │   │   │   │   │   │   │   └── MapSelectionScreen.kt
│   │   │   │   │   │   │   └── shared/
│   │   │   │   │   │   │       ├── ItineraryCard.kt
│   │   │   │   │   │   │       ├── ActivityItem.kt
│   │   │   │   │   │   │       ├── MapComposable.kt
│   │   │   │   │   │   │       └── ShareBottomSheet.kt
│   │   │   │   │   │   │
│   │   │   │   │   │   ├── bookings/
│   │   │   │   │   │   │   ├── list/
│   │   │   │   │   │   │   │   ├── BookingsScreen.kt
│   │   │   │   │   │   │   │   └── BookingsViewModel.kt
│   │   │   │   │   │   │   ├── detail/
│   │   │   │   │   │   │   │   ├── BookingDetailScreen.kt
│   │   │   │   │   │   │   │   └── BookingDetailViewModel.kt
│   │   │   │   │   │   │   ├── checkout/
│   │   │   │   │   │   │   │   ├── CheckoutScreen.kt
│   │   │   │   │   │   │   │   ├── CheckoutViewModel.kt
│   │   │   │   │   │   │   │   ├── PaymentScreen.kt
│   │   │   │   │   │   │   │   └── ConfirmationScreen.kt
│   │   │   │   │   │   │   └── shared/
│   │   │   │   │   │   │       ├── BookingCard.kt
│   │   │   │   │   │   │       └── PaymentMethodSelector.kt
│   │   │   │   │   │   │
│   │   │   │   │   │   ├── explore/
│   │   │   │   │   │   │   ├── ExploreScreen.kt
│   │   │   │   │   │   │   ├── ExploreViewModel.kt
│   │   │   │   │   │   │   ├── SearchScreen.kt
│   │   │   │   │   │   │   ├── FilterScreen.kt
│   │   │   │   │   │   │   ├── DestinationGrid.kt
│   │   │   │   │   │   │   ├── DestinationDetailScreen.kt
│   │   │   │   │   │   │   └── CategoryScreen.kt
│   │   │   │   │   │   │
│   │   │   │   │   │   ├── ai/
│   │   │   │   │   │   │   ├── AIChatScreen.kt
│   │   │   │   │   │   │   ├── AIChatViewModel.kt
│   │   │   │   │   │   │   ├── ChatMessageComposable.kt
│   │   │   │   │   │   │   ├── SuggestionCard.kt
│   │   │   │   │   │   │   ├── TypingAnimation.kt
│   │   │   │   │   │   │   └── MessageInput.kt
│   │   │   │   │   │   │
│   │   │   │   │   │   └── settings/
│   │   │   │   │   │       ├── SettingsScreen.kt
│   │   │   │   │   │       ├── SettingsViewModel.kt
│   │   │   │   │   │       ├── ProfileSettingsScreen.kt
│   │   │   │   │   │       ├── NotificationPreferencesScreen.kt
│   │   │   │   │   │       ├── PrivacySettingsScreen.kt
│   │   │   │   │   │       └── AboutScreen.kt
│   │   │   │   │   │
│   │   │   │   │   ├── components/
│   │   │   │   │   │   ├── common/
│   │   │   │   │   │   │   ├── TopAppBar.kt
│   │   │   │   │   │   │   ├── BottomNavigationBar.kt
│   │   │   │   │   │   │   ├── LoadingIndicator.kt
│   │   │   │   │   │   │   ├── ErrorScreen.kt
│   │   │   │   │   │   │   ├── EmptyState.kt
│   │   │   │   │   │   │   └── SnackbarController.kt
│   │   │   │   │   │   │
│   │   │   │   │   │   ├── ui/
│   │   │   │   │   │   │   ├── CustomButton.kt
│   │   │   │   │   │   │   ├── CustomTextField.kt
│   │   │   │   │   │   │   ├── CustomCard.kt
│   │   │   │   │   │   │   ├── CustomDropdown.kt
│   │   │   │   │   │   │   ├── RatingBar.kt
│   │   │   │   │   │   │   ├── PriceTag.kt
│   │   │   │   │   │   │   └── LocationChip.kt
│   │   │   │   │   │   │
│   │   │   │   │   │   └── dialogs/
│   │   │   │   │   │       ├── ConfirmDialog.kt
│   │   │   │   │   │       ├── DatePickerDialog.kt
│   │   │   │   │   │       ├── TimePickerDialog.kt
│   │   │   │   │   │       └── BottomSheetDialog.kt
│   │   │   │   │   │
│   │   │   │   │   └── utils/
│   │   │   │   │       ├── PreviewParameterProvider.kt
│   │   │   │   │       ├── ComposablePreview.kt
│   │   │   │   │       └── Theme Preview.kt
│   │   │   │   │
│   │   │   │   ├── domain/
│   │   │   │   │   ├── models/
│   │   │   │   │   │   ├── User.kt
│   │   │   │   │   │   ├── Itinerary.kt
│   │   │   │   │   │   ├── Activity.kt
│   │   │   │   │   │   ├── Destination.kt
│   │   │   │   │   │   ├── Booking.kt
│   │   │   │   │   │   ├── Review.kt
│   │   │   │   │   │   └── Result.kt (sealed class)
│   │   │   │   │   │
│   │   │   │   │   ├── repositories/
│   │   │   │   │   │   ├── AuthRepository.kt
│   │   │   │   │   │   ├── ItineraryRepository.kt
│   │   │   │   │   │   ├── BookingRepository.kt
│   │   │   │   │   │   ├── UserRepository.kt
│   │   │   │   │   │   └── AIRepository.kt
│   │   │   │   │   │
│   │   │   │   │   ├── usecases/
│   │   │   │   │   │   ├── auth/
│   │   │   │   │   │   │   ├── LoginUseCase.kt
│   │   │   │   │   │   │   ├── SignupUseCase.kt
│   │   │   │   │   │   │   └── LogoutUseCase.kt
│   │   │   │   │   │   ├── itinerary/
│   │   │   │   │   │   │   ├── GetItinerariesUseCase.kt
│   │   │   │   │   │   │   ├── CreateItineraryUseCase.kt
│   │   │   │   │   │   │   ├── UpdateItineraryUseCase.kt
│   │   │   │   │   │   │   └── DeleteItineraryUseCase.kt
│   │   │   │   │   │   └── booking/
│   │   │   │   │   │       ├── GetBookingsUseCase.kt
│   │   │   │   │   │       ├── CreateBookingUseCase.kt
│   │   │   │   │   │       └── CancelBookingUseCase.kt
│   │   │   │   │   │
│   │   │   │   │   └── exceptions/
│   │   │   │   │       ├── NetworkException.kt
│   │   │   │   │       ├── LocalException.kt
│   │   │   │   │       ├── ParseException.kt
│   │   │   │   │       └── UnauthorizedException.kt
│   │   │   │   │
│   │   │   │   ├── data/
│   │   │   │   │   ├── remote/
│   │   │   │   │   │   ├── api/
│   │   │   │   │   │   │   ├── ApiClient.kt
│   │   │   │   │   │   │   ├── AuthApi.kt
│   │   │   │   │   │   │   ├── ItineraryApi.kt
│   │   │   │   │   │   │   ├── BookingApi.kt
│   │   │   │   │   │   │   ├── UserApi.kt
│   │   │   │   │   │   │   └── AiApi.kt
│   │   │   │   │   │   ├── dto/
│   │   │   │   │   │   │   ├── ApiResponse.kt
│   │   │   │   │   │   │   ├── AuthRequest.kt
│   │   │   │   │   │   │   ├── AuthResponse.kt
│   │   │   │   │   │   │   ├── ItineraryRequest.kt
│   │   │   │   │   │   │   ├── ItineraryResponse.kt
│   │   │   │   │   │   │   └── BookingRequest.kt
│   │   │   │   │   │   ├── interceptors/
│   │   │   │   │   │   │   ├── AuthInterceptor.kt
│   │   │   │   │   │   │   ├── LoggingInterceptor.kt
│   │   │   │   │   │   │   └── ErrorInterceptor.kt
│   │   │   │   │   │   └── serializer/
│   │   │   │   │   │       ├── DateSerializer.kt
│   │   │   │   │   │       └── CustomSerializers.kt
│   │   │   │   │   │
│   │   │   │   │   ├── local/
│   │   │   │   │   │   ├── database/
│   │   │   │   │   │   │   ├── YatraDiscoverDb.kt (Room Database)
│   │   │   │   │   │   │   ├── dao/
│   │   │   │   │   │   │   │   ├── ItineraryDao.kt
│   │   │   │   │   │   │   │   ├── UserDao.kt
│   │   │   │   │   │   │   │   ├── BookingDao.kt
│   │   │   │   │   │   │   │   └── CacheDao.kt
│   │   │   │   │   │   │   └── entities/
│   │   │   │   │   │   │       ├── ItineraryEntity.kt
│   │   │   │   │   │   │       ├── UserEntity.kt
│   │   │   │   │   │   │       ├── BookingEntity.kt
│   │   │   │   │   │   │       └── ActivityEntity.kt
│   │   │   │   │   │   │
│   │   │   │   │   │   ├── preferences/
│   │   │   │   │   │   │   ├── UserPreferencesDataStore.kt
│   │   │   │   │   │   │   ├── AppPreferencesDataStore.kt
│   │   │   │   │   │   │   └── PreferencesManager.kt
│   │   │   │   │   │   │
│   │   │   │   │   │   └── cache/
│   │   │   │   │   │       ├── CacheManager.kt
│   │   │   │   │   │       └── CachePolicy.kt
│   │   │   │   │   │
│   │   │   │   │   ├── repositories/
│   │   │   │   │   │   ├── AuthRepositoryImpl.kt
│   │   │   │   │   │   ├── ItineraryRepositoryImpl.kt
│   │   │   │   │   │   ├── BookingRepositoryImpl.kt
│   │   │   │   │   │   ├── UserRepositoryImpl.kt
│   │   │   │   │   │   └── AIRepositoryImpl.kt
│   │   │   │   │   │
│   │   │   │   │   └── mappers/
│   │   │   │   │       ├── EntityMapper.kt
│   │   │   │   │       ├── DtoMapper.kt
│   │   │   │   │       └── DataMapper.kt
│   │   │   │   │
│   │   │   │   └── utils/
│   │   │   │       ├── extensions/
│   │   │   │       │   ├── String.kt
│   │   │   │       │   ├── Date.kt
│   │   │   │       │   ├── Flow.kt
│   │   │   │       │   ├── Modifier.kt
│   │   │   │       │   └── Context.kt
│   │   │   │       │
│   │   │   │       ├── helpers/
│   │   │   │       │   ├── DateFormatter.kt
│   │   │   │       │   ├── CurrencyFormatter.kt
│   │   │   │       │   ├── ValidationHelper.kt
│   │   │   │       │   └── ImageLoader.kt
│   │   │   │       │
│   │   │   │       ├── constants/
│   │   │   │       │   ├── ApiConstants.kt
│   │   │   │       │   ├── AppConstants.kt
│   │   │   │       │   ├── UiConstants.kt
│   │   │   │       │   └── EnvironmentVariables.kt
│   │   │   │       │
│   │   │   │       └── services/
│   │   │   │           ├── LocationService.kt
│   │   │   │           ├── NotificationService.kt
│   │   │   │           ├── AnalyticsService.kt
│   │   │   │           └── ConnectivityService.kt
│   │   │   │
│   │   │   └── res/
│   │   │       ├── drawable/
│   │   │       ├── mipmap/
│   │   │       ├── values/
│   │   │       │   ├── colors.xml
│   │   │       │   ├── strings.xml
│   │   │       │   ├── dimens.xml
│   │   │       │   └── styles.xml
│   │   │       └── xml/
│   │   │
│   │   ├── test/
│   │   │   └── java/com/yatradiscover/
│   │   │       ├── viewmodel/
│   │   │       │   ├── LoginViewModelTest.kt
│   │   │       │   ├── ItineraryViewModelTest.kt
│   │   │       │   └── BookingViewModelTest.kt
│   │   │       ├── repository/
│   │   │       │   ├── AuthRepositoryTest.kt
│   │   │       │   └── ItineraryRepositoryTest.kt
│   │   │       ├── usecase/
│   │   │       │   └── LoginUseCaseTest.kt
│   │   │       └── utils/
│   │   │           └── ValidationHelperTest.kt
│   │   │
│   │   └── androidTest/
│   │       └── java/com/yatradiscover/
│   │           ├── ui/
│   │           │   ├── AuthenticationFlowTest.kt
│   │           │   ├── ItineraryCreationFlowTest.kt
│   │           │   └── BookingFlowTest.kt
│   │           └── screens/
│   │               └── LoginScreenTest.kt
│   │
│   └── build.gradle.kts
│
├── build-logic/
│   ├── build.gradle.kts
│   └── src/main/kotlin/
│       └── com/yatradiscover/
│           └── build/
│               ├── AndroidConfigPlugin.kt
│               ├── HiltPlugin.kt
│               └── ComposePlugin.kt
│
├── build.gradle.kts (Root)
├── settings.gradle.kts
├── gradle.properties
├── .gitignore
├── .editorconfig
├── lint.xml
├── detekt.yml
├── README.md
└── ARCHITECTURE.md
```

## Jetpack Compose Best Practices

### Composable Functions

```kotlin
// Avoid using multiple state hoisting
@Composable
fun ItineraryCard(
    itinerary: Itinerary,
    onEdit: (Itinerary) -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .padding(16.dp),
        shape = RoundedCornerShape(12.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = itinerary.title,
                style = MaterialTheme.typography.headlineSmall,
                color = MaterialTheme.colorScheme.primary
            )
            // ... content
        }
    }
}
```

### ViewModel Integration

```kotlin
@HiltViewModel
class ItineraryListViewModel @Inject constructor(
    private val getItinerariesUseCase: GetItinerariesUseCase
) : ViewModel() {
    
    private val _state = MutableStateFlow<ItineraryListState>(ItineraryListState.Loading)
    val state: StateFlow<ItineraryListState> = _state.asStateFlow()
    
    init {
        loadItineraries()
    }
    
    private fun loadItineraries() {
        viewModelScope.launch {
            getItinerariesUseCase()
                .collect { result ->
                    _state.value = when (result) {
                        is Result.Success -> ItineraryListState.Success(result.data)
                        is Result.Error -> ItineraryListState.Error(result.exception.message ?: "")
                        is Result.Loading -> ItineraryListState.Loading
                    }
                }
        }
    }
}
```

### State Management Pattern

```kotlin
sealed class ItineraryListState {
    object Loading : ItineraryListState()
    data class Success(val itineraries: List<Itinerary>) : ItineraryListState()
    data class Error(val message: String) : ItineraryListState()
}

@Composable
fun ItineraryListScreen(viewModel: ItineraryListViewModel = hiltViewModel()) {
    val state by viewModel.state.collectAsState()
    
    when (state) {
        is ItineraryListState.Loading -> LoadingIndicator()
        is ItineraryListState.Success -> {
            val itineraries = (state as ItineraryListState.Success).itineraries
            ItineraryList(itineraries)
        }
        is ItineraryListState.Error -> {
            val message = (state as ItineraryListState.Error).message
            ErrorScreen(message)
        }
    }
}
```

## Hilt Dependency Injection

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    
    @Singleton
    @Provides
    fun provideApiClient(): ApiClient {
        return ApiClient(
            baseUrl = BuildConfig.API_BASE_URL,
            interceptors = listOf(
                AuthInterceptor(),
                LoggingInterceptor()
            )
        )
    }
    
    @Singleton
    @Provides
    fun provideItineraryRepository(
        apiClient: ApiClient,
        database: YatraDiscoverDb
    ): ItineraryRepository {
        return ItineraryRepositoryImpl(apiClient, database)
    }
}
```

## Navigation

```kotlin
@Composable
fun YatraDiscoverNavGraph() {
    val navController = rememberNavController()
    
    NavHost(navController, startDestination = Screen.Splash.route) {
        composable(Screen.Splash.route) {
            SplashScreen(
                onNavigateToAuth = {
                    navController.navigate(Screen.Login.route)
                },
                onNavigateToDashboard = {
                    navController.navigate(Screen.Dashboard.route) {
                        popUpTo(Screen.Splash.route) { inclusive = true }
                    }
                }
            )
        }
        
        authNavGraph(navController)
        dashboardNavGraph(navController)
    }
}
```

## Testing Examples

### Unit Test

```kotlin
@RunWith(RobolectricTestRunner::class)
class LoginViewModelTest {
    
    @get:Rule
    val instantExecutorRule = InstantTaskExecutorRule()
    
    private lateinit var viewModel: LoginViewModel
    private val loginUseCase = mockk<LoginUseCase>()
    
    @Before
    fun setUp() {
        viewModel = LoginViewModel(loginUseCase)
    }
    
    @Test
    fun loginSuccess() = runTest {
        // Arrange
        val user = User(id = "1", email = "test@example.com")
        coEvery { loginUseCase(any()) } returns flowOf(Result.Success(user))
        
        // Act
        viewModel.login("test@example.com", "password")
        
        // Assert
        viewModel.state.test {
            assertThat(awaitItem()).isInstanceOf(LoginState.Success::class.java)
        }
    }
}
```

### UI Test (Espresso)

```kotlin
@RunWith(AndroidJUnit4::class)
class LoginScreenTest {
    
    @get:Rule
    val composeRule = createAndroidComposeRule<MainActivity>()
    
    @Test
    fun loginScreenDisplaysCorrectly() {
        composeRule.setContent {
            LoginScreen()
        }
        
        composeRule.onNodeWithText("Email").assertExists()
        composeRule.onNodeWithText("Password").assertExists()
        composeRule.onNodeWithText("Login").assertExists()
    }
}
```

## Performance Optimization

### Remember & Recomposition

```kotlin
@Composable
fun ItineraryList(itineraries: List<Itinerary>) {
    // Only recompose when itineraries list changes
    val memoizedList = remember(itineraries) { itineraries }
    
    LazyColumn {
        items(memoizedList, key = { it.id }) { itinerary ->
            ItineraryCard(itinerary)
        }
    }
}
```

### Stable Classes

```kotlin
// Mark data classes as stable for better Compose optimization
@Stable
data class Itinerary(
    val id: String,
    val title: String,
    val description: String,
    val startDate: LocalDate,
    val endDate: LocalDate
)
```

---

**Last Updated:** 2026-11-13
**Status:** Ready for development

#include <atlbase.h>
#include <ShObjIdl.h>
#include <string>

#define FSDEVMODELAUNCHER_MAJOR_VERSION 1
#define FSDEVMODELAUNCHER_MINOR_VERSION 0

struct COMInitRAII
{
	HRESULT	hr;
	COMInitRAII()
	{
		hr = CoInitializeEx(nullptr, COINIT_APARTMENTTHREADED);
		if (FAILED(hr))
			fwprintf_s(stderr, L"Error: failed to init COM. hr = 0x%08lx \n", hr);
	}

	~COMInitRAII()
	{
		CoUninitialize();
	}
};

std::wstring BuildArguments()
{
	std::wstring wArgs;
	wArgs = L"-FastLaunch";
	return wArgs;
}

int main(int argc, char* argv[])
{
	COMInitRAII comInit;
	if (FAILED(comInit.hr))
		return EXIT_FAILURE;

	HRESULT hr = S_OK;

	CComPtr<IApplicationActivationManager> AppActivationMgr = nullptr;
	hr = CoCreateInstance(CLSID_ApplicationActivationManager, nullptr, CLSCTX_LOCAL_SERVER, IID_PPV_ARGS(&AppActivationMgr));
	if (FAILED(hr))
	{
		fwprintf_s(stderr, L"Error: failed to create Application Activation Manager. hr = 0x%08lx \n", hr);
		return EXIT_FAILURE;
	}

	const std::wstring wArgs = BuildArguments();

	static LPCWSTR appUserModelIDList[] = {
		L"Microsoft.Limitless_8wekyb3d8bbwe!App",
	};

	LPCWSTR appUserModelID = NULL;

	DWORD dwProcessId = 0;
	for (int curAppIdx = 0; curAppIdx < _countof(appUserModelIDList); curAppIdx++)
	{
		appUserModelID = appUserModelIDList[curAppIdx];
		hr = AppActivationMgr->ActivateApplication(appUserModelID, wArgs.c_str(), AO_NOERRORUI, &dwProcessId);
		if (SUCCEEDED(hr))
			break;
	}

	if (FAILED(hr))
	{
		fwprintf_s(stderr, L"Error: Failed to Activate App %s. hr = 0x%08lx \n", appUserModelID, hr);
		return EXIT_FAILURE;
	}

	HANDLE hProcess = ::OpenProcess(SYNCHRONIZE, FALSE, dwProcessId);
	if (hProcess == NULL)
	{
		fwprintf_s(stderr, L"Error: Failed to open process for synchronization: pid = %d \n", dwProcessId);
		return EXIT_FAILURE;
	}

	::WaitForSingleObject(hProcess, INFINITE);

	DWORD exitCode = 0;
	if (::GetExitCodeProcess(hProcess, &exitCode))
		return exitCode;

	::CloseHandle(hProcess);

	return EXIT_FAILURE;
}

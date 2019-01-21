package canonchain;

import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.io.*;

public class FileReader
{

	public static void main(String[] args)
	{

		String filePathStr = args[0];
		String MatchPatternStr = args[1];
		File file = new File(filePathStr);
		String str;
		List<String> lss = new ArrayList<String>();
		List<String> lStrings = new ArrayList<String>();
		String capturedFilePath = file.getParent() + "\\cap.txt";
		File capturedFile = new File(capturedFilePath);

		try
		{
			BufferedReader bufferedReader = new BufferedReader(
					new InputStreamReader(new FileInputStream(file), "utf-8"));
			while ((str = bufferedReader.readLine()) != null)
			{

				lStrings = MatchMethod(MatchPatternStr, lss, str);
			}
			bufferedReader.close();
		} catch (Exception e)
		{
			e.printStackTrace();
		}

		try
		{
			capturedFile.createNewFile();

//			BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(capturedFile));
			BufferedOutputStream bufferedOutputStream = new BufferedOutputStream(
					new FileOutputStream(capturedFile, true));

//			syntax sugar;			
			lStrings.forEach((lString) ->
			{
				try
				{

//					bufferedWriter.write(lString);
					bufferedOutputStream.write(lString.getBytes());

				} catch (IOException e)
				{

					e.printStackTrace();
				}
			});

//			bufferedWriter.close();
			bufferedOutputStream.close();
		} catch (IOException e)
		{
			e.printStackTrace();
		}

		for (int i = 0; i < args.length; i++)
		{
			System.out.println(i + " " + args[i]);
		}
	}

	private static List<String> MatchMethod(String MatchPattern, List<String> lstrs, String content)
	{

		Pattern pattern = Pattern.compile(".*" + MatchPattern + ".*", Pattern.CASE_INSENSITIVE);

		Matcher matcher = pattern.matcher(content);

		while (matcher.find())
		{
			lstrs.add(matcher.group(0) + "\n");
		}
		return lstrs;
	}

}
